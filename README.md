# PBIL Python Wrapper

A Python wrapper around a high-performance C implementation of **Population Based Incremental Learning (PBIL)** for solving MAXSAT problems.

## About

This project provides a clean Python interface to an existing, optimized C implementation of the PBIL algorithm. The wrapper maintains the full performance of the original C code while offering modern Python conveniences for parameter tuning, result analysis, and integration into larger systems.

### Key Features

- **🚀 High Performance**: Direct calls to optimized C implementation
- **🐍 Python Friendly**: Clean, intuitive Python API
- **🔧 Auto-compilation**: Automatically compiles C source when needed
- **📊 Rich Output**: Structured results with detailed statistics
- **🎯 Robust**: Comprehensive error handling and memory management
- **📱 CLI Support**: Command-line interface for quick experimentation

## What is PBIL?

Population Based Incremental Learning (PBIL) is an evolutionary algorithm that combines concepts from genetic algorithms and competitive learning. Instead of maintaining a population of individuals, PBIL maintains a probability vector that represents the distribution of good solutions. This approach is particularly effective for discrete optimization problems like MAXSAT.

### Algorithm Overview

1. **Initialization**: Start with a probability vector (typically all 0.5)
2. **Generation**: Sample individuals from the probability vector
3. **Selection**: Identify best and worst individuals
4. **Learning**: Update probability vector toward good solutions, away from bad ones
5. **Mutation**: Apply small random perturbations
6. **Repeat**: Continue until optimal solution found or max iterations reached

## Installation

### Prerequisites

- Python 3.7+
- GCC compiler (for automatic C compilation)
- Standard C libraries

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd evolution_simulation
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package** (optional):
   ```bash
   pip install -e .
   ```

The C code will be automatically compiled when first used.

## Quick Start

### Basic Usage

```python
from evolution_simulation.pbil import run_pbil

# Solve a MAXSAT problem
result = run_pbil('problem.cnf', max_iterations=1000)

print(f"Solution: {result['best_solution']}")
print(f"Fitness: {result['fitness']}/{result['max_fitness']}")
print(f"Success: {result['success']}")
```

### Advanced Usage

```python
from evolution_simulation.pbil import PBILWrapper

# Create wrapper instance
pbil = PBILWrapper()

# Run with custom parameters
result = pbil.run(
    cnf_file='problem.cnf',
    pop_size=100,
    learning_rate=0.1,
    negative_learning_rate=0.075,
    mutation_probability=0.02,
    mutation_shift=0.05,
    max_iterations=1000,
    print_generations=True
)

# Pretty print results
pbil.print_results(result)
```

### Command Line Interface

```bash
# Basic usage
python evolution_simulation/pbil.py problem.cnf

# With custom parameters
python evolution_simulation/pbil.py problem.cnf \
  --pop-size 200 \
  --learning-rate 0.15 \
  --max-iterations 2000 \
  --print-generations
```

## API Reference

### PBILWrapper Class

The main wrapper class providing full control over the PBIL algorithm.

#### Methods

##### `__init__(executable_path=None)`
Initialize the wrapper. Automatically finds or compiles the C executable.

##### `run(**kwargs)` → `Dict[str, Any]`
Run the PBIL algorithm with specified parameters.

**Parameters:**
- `cnf_file` (str): Path to CNF file containing MAXSAT problem
- `pop_size` (int, default=100): Population size
- `learning_rate` (float, default=0.1): Learning rate for probability vector updates
- `negative_learning_rate` (float, default=0.075): Negative learning rate
- `mutation_probability` (float, default=0.02): Probability of mutation per bit
- `mutation_shift` (float, default=0.05): Magnitude of mutation
- `max_iterations` (int, default=1000): Maximum number of generations
- `print_generations` (bool, default=False): Print progress during execution

**Returns:** Dictionary with results including:
- `success` (bool): Whether optimal solution was found
- `best_solution` (List[int]): Best solution found
- `fitness` (int): Number of satisfied clauses
- `max_fitness` (int): Total number of clauses
- `fitness_percentage` (float): Percentage of clauses satisfied
- `total_generations` (int): Number of generations executed
- `time_elapsed` (float): Runtime in seconds
- `best_found_at_generation` (int): Generation where best solution was found

##### `run_multiple(cnf_files, **kwargs)` → `List[Dict[str, Any]]`
Run PBIL on multiple CNF files with the same parameters.

##### `print_results(results)`
Pretty print formatted results.

### Convenience Functions

##### `run_pbil(cnf_file, **kwargs)` → `Dict[str, Any]`
Quick function to run PBIL with default parameters.

## CNF File Format

The wrapper accepts CNF (Conjunctive Normal Form) files in DIMACS format:

```
c This is a comment
p cnf 3 3
1 -2 3 0
-1 2 -3 0  
1 2 3 0
```

- Line starting with `c`: Comments
- Line starting with `p cnf`: Problem definition (variables, clauses)
- Other lines: Clauses (space-separated literals, 0-terminated)

## Examples

### Parameter Tuning

```python
from evolution_simulation.pbil import PBILWrapper

wrapper = PBILWrapper()

# Test different strategies
strategies = [
    {"name": "Conservative", "learning_rate": 0.05, "pop_size": 50},
    {"name": "Balanced", "learning_rate": 0.1, "pop_size": 100},
    {"name": "Aggressive", "learning_rate": 0.2, "pop_size": 200},
]

for strategy in strategies:
    name = strategy.pop("name")
    result = wrapper.run(cnf_file="problem.cnf", **strategy)
    print(f"{name}: {result['fitness']}/{result['max_fitness']}")
```

### Batch Processing

```python
import glob
from evolution_simulation.pbil import PBILWrapper

wrapper = PBILWrapper()
cnf_files = glob.glob("problems/*.cnf")

results = wrapper.run_multiple(cnf_files, max_iterations=500)

for result in results:
    if result['success']:
        print(f"✅ {result['cnf_file']}: SOLVED")
    else:
        print(f"⚠️ {result['cnf_file']}: {result['fitness']}/{result['max_fitness']}")
```

## Architecture

This wrapper is built around your existing C implementation with the following components:

- **C Core** (`c_src/`): Original high-performance PBIL implementation
- **Python Wrapper** (`evolution_simulation/pbil.py`): Subprocess-based interface
- **Auto-compilation**: Automatic GCC compilation of C sources
- **Output Parsing**: Regex-based extraction of results from C program output

### Project Structure

```
evolution_simulation/
├── c_src/                    # Original C implementation
│   ├── pbil_c.c             # Main PBIL algorithm
│   ├── dependencies.c       # CNF parsing and fitness evaluation
│   ├── c_helper_functions.c # Core PBIL functions
│   └── *.h                  # Header files
├── evolution_simulation/     # Python package
│   ├── pbil.py              # Main wrapper class
│   └── maxsat_problem.py    # Problem utilities
├── main.py                  # Demonstration script
└── sample_problem.cnf       # Example problem
```

## Performance

The wrapper calls your original C implementation directly via subprocess, providing:

- **Full C Performance**: No overhead from Python-C integration
- **Memory Efficiency**: C manages its own memory
- **Scalability**: Can handle large problems efficiently
- **Reliability**: Fixed memory management issues (double-free bugs)

## Contributing

This wrapper preserves the original C implementation while adding Python conveniences. To contribute:

1. For C algorithm improvements, modify files in `c_src/`
2. For Python interface improvements, modify `evolution_simulation/pbil.py`
3. Ensure all changes maintain backward compatibility
4. Add tests for new functionality

## License

[Add your license information here]

## Original Implementation

This wrapper is built around the C implementation from: https://github.com/patrick-callum-oconnell-builder/Population-Based-Incremental-Learning

The original README stated: "PBIL.py is no longer used" and "I've since converted it to C for speed." This wrapper brings Python convenience back while preserving that C performance. 