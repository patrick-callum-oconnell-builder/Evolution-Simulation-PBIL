"""
FastAPI Backend for Real-time PBIL Visualization

Provides WebSocket endpoints for streaming live PBIL algorithm progress
and REST endpoints for configuration and control.
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional, List
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Add parent directories to path to import our PBIL wrapper
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Change working directory to project root so C compilation can find files
original_cwd = os.getcwd()
os.chdir(project_root)

from evolution_simulation.pbil import PBILWrapper


# Initialize FastAPI app
app = FastAPI(title="PBIL Real-time Visualization API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (React build)
frontend_build_path = Path(__file__).parent.parent / "frontend" / "build"
if frontend_build_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_build_path / "static")), name="static")


class PBILConfig(BaseModel):
    """Configuration model for PBIL parameters."""
    cnf_file: str = "sample_problem.cnf"
    pop_size: int = 100
    learning_rate: float = 0.1
    negative_learning_rate: float = 0.075
    mutation_probability: float = 0.02
    mutation_shift: float = 0.05
    max_iterations: int = 1000


class PBILProgress(BaseModel):
    """Model for PBIL progress updates."""
    generation: int
    best_fitness: int
    max_fitness: int
    best_individual: List[int]
    worst_individual: List[int]
    probability_vector: List[float]
    is_complete: bool = False
    time_elapsed: float = 0.0


class RealtimePBILWrapper(PBILWrapper):
    """Enhanced PBIL wrapper that supports real-time streaming."""
    
    def __init__(self):
        super().__init__()
        self.websocket: Optional[WebSocket] = None
        self.is_running = False
        
    async def run_realtime(self, config: PBILConfig, websocket: WebSocket) -> Dict[str, Any]:
        """Run PBIL with real-time WebSocket updates."""
        self.websocket = websocket
        self.is_running = True
        
        try:
            await websocket.send_json({
                "type": "status", 
                "message": "Starting PBIL algorithm...",
                "config": config.dict()
            })
            
            # Prepare arguments for the C program
            args = [
                self.executable_path,
                str(config.pop_size),
                str(config.learning_rate),
                str(config.negative_learning_rate),
                str(config.mutation_probability),
                str(config.mutation_shift),
                str(config.max_iterations),
                config.cnf_file,
                "1"  # Enable generation printing
            ]
            
            # Start the C process
            import subprocess
            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Stream output line by line
            generation_data = {}
            current_gen = 0
            
            async for line in self._stream_output(process):
                if not self.is_running:
                    process.terminate()
                    break
                    
                # Parse line for PBIL data
                update = self._parse_line(line, generation_data, current_gen)
                if update:
                    await websocket.send_json({
                        "type": "progress",
                        "data": update.dict()
                    })
                    if update.generation > current_gen:
                        current_gen = update.generation
            
            # Wait for process completion
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                # Parse final results
                final_result = self._parse_output(stdout, config.cnf_file)
                await websocket.send_json({
                    "type": "complete",
                    "data": final_result
                })
                return final_result
            else:
                raise RuntimeError(f"PBIL execution failed: {stderr}")
                
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
            raise
        finally:
            self.is_running = False
    
    async def _stream_output(self, process):
        """Stream process output line by line."""
        while True:
            line = process.stdout.readline()
            if not line:
                break
            yield line.strip()
            await asyncio.sleep(0.01)  # Small delay to prevent overwhelming
    
    def _parse_line(self, line: str, gen_data: dict, current_gen: int) -> Optional[PBILProgress]:
        """Parse a single line of output for generation data."""
        import re
        
        # Match generation header
        gen_match = re.match(r'Generation: (\d+)', line)
        if gen_match:
            gen_data['generation'] = int(gen_match.group(1))
            return None
        
        # Match best individual
        best_match = re.match(r'Best individual: <(.+)>', line)
        if best_match:
            individuals = [int(x) for x in best_match.group(1).strip().split()]
            gen_data['best_individual'] = individuals
            return None
            
        # Match worst individual
        worst_match = re.match(r'Worst individual: <(.+)>', line)
        if worst_match:
            individuals = [int(x) for x in worst_match.group(1).strip().split()]
            gen_data['worst_individual'] = individuals
            return None
        
        # Match probability vector
        prob_match = re.match(r'Probability Vector: <(.+)>', line)
        if prob_match:
            probs = [float(x) for x in prob_match.group(1).strip().split()]
            gen_data['probability_vector'] = probs
            
            # If we have all data for this generation, create progress update
            if all(key in gen_data for key in ['generation', 'best_individual', 'probability_vector']):
                progress = PBILProgress(
                    generation=gen_data['generation'],
                    best_fitness=sum(gen_data['best_individual']),  # Simplified fitness
                    max_fitness=len(gen_data['best_individual']),   # Placeholder
                    best_individual=gen_data['best_individual'],
                    worst_individual=gen_data.get('worst_individual', []),
                    probability_vector=gen_data['probability_vector']
                )
                gen_data.clear()  # Reset for next generation
                return progress
        
        # Check for completion
        if "Reached max fitness" in line:
            return PBILProgress(
                generation=current_gen,
                best_fitness=0,
                max_fitness=0,
                best_individual=[],
                worst_individual=[],
                probability_vector=[],
                is_complete=True
            )
        
        return None
    
    def stop(self):
        """Stop the running PBIL process."""
        self.is_running = False


# Global wrapper instance
pbil_wrapper = RealtimePBILWrapper()


class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                # Remove broken connections
                self.disconnect(connection)


manager = ConnectionManager()


@app.get("/")
async def root():
    """Serve the React app."""
    frontend_path = frontend_build_path / "index.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    return {"message": "PBIL Real-time Visualization API", "status": "running"}


@app.get("/api/status")
async def get_status():
    """Get current API status."""
    return {
        "status": "running",
        "pbil_running": pbil_wrapper.is_running,
        "executable_available": pbil_wrapper.executable_path is not None,
        "working_directory": os.getcwd()
    }


@app.get("/api/cnf-files")
async def list_cnf_files():
    """List available CNF files."""
    cnf_files = []
    
    for file_path in Path(".").glob("*.cnf"):
        cnf_files.append({
            "name": file_path.name,
            "path": str(file_path),
            "size": file_path.stat().st_size
        })
    
    return {"files": cnf_files}


@app.post("/api/pbil/run")
async def run_pbil(config: PBILConfig):
    """Start a PBIL run (non-realtime)."""
    if pbil_wrapper.is_running:
        raise HTTPException(status_code=409, detail="PBIL is already running")
    
    try:
        result = pbil_wrapper.run(
            cnf_file=config.cnf_file,
            pop_size=config.pop_size,
            learning_rate=config.learning_rate,
            negative_learning_rate=config.negative_learning_rate,
            mutation_probability=config.mutation_probability,
            mutation_shift=config.mutation_shift,
            max_iterations=config.max_iterations,
            print_generations=False
        )
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/pbil/stop")
async def stop_pbil():
    """Stop the running PBIL process."""
    pbil_wrapper.stop()
    await manager.broadcast({"type": "stopped", "message": "PBIL execution stopped"})
    return {"success": True, "message": "PBIL stopped"}


@app.websocket("/ws/test")
async def websocket_test(websocket: WebSocket):
    """Simple test WebSocket endpoint."""
    await websocket.accept()
    await websocket.send_text("Hello from test WebSocket!")
    await websocket.close()


@app.websocket("/ws/pbil")
async def websocket_pbil(websocket: WebSocket):
    """WebSocket endpoint for real-time PBIL streaming."""
    await manager.connect(websocket)
    
    try:
        while True:
            # Wait for configuration from client
            data = await websocket.receive_json()
            
            if data.get("action") == "start":
                if pbil_wrapper.is_running:
                    await websocket.send_json({
                        "type": "error",
                        "message": "PBIL is already running"
                    })
                    continue
                
                try:
                    config = PBILConfig(**data.get("config", {}))
                    await pbil_wrapper.run_realtime(config, websocket)
                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })
            
            elif data.get("action") == "stop":
                pbil_wrapper.stop()
                await websocket.send_json({
                    "type": "stopped",
                    "message": "PBIL execution stopped"
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        pbil_wrapper.stop()


def start_server():
    """Start the uvicorn server programmatically."""
    import uvicorn
    print("🚀 Starting PBIL Backend Server...")
    print("📍 API available at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs") 
    print("🔌 WebSocket: ws://localhost:8000/ws/pbil")
    print("-" * 50)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    start_server() 