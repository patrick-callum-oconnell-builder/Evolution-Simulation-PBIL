#!/usr/bin/env python3
"""
PBIL Wrapper Demonstration

This script demonstrates the Python wrapper around the high-performance C implementation
of Population Based Incremental Learning (PBIL) for solving MAXSAT problems.

The wrapper provides a clean Python interface while leveraging the full speed of the
original C implementation.
"""

import os
import time
from evolution_simulation.pbil import PBILWrapper, run_pbil


def main():
    """Main demonstration of the PBIL wrapper."""
    print("🧬 PBIL (Population Based Incremental Learning) Wrapper Demo")
    print("=" * 60)
    
    # Check if sample problem exists
    sample_file = "sample_problem.cnf"
    if not os.path.exists(sample_file):
        print(f"❌ Sample file {sample_file} not found!")
        return
    
    print(f"📄 Using sample problem: {sample_file}")
    print()
    
    # 1. Simple usage with convenience function
    print("1️⃣  Simple Usage (Convenience Function)")
    print("-" * 40)
    
    result = run_pbil(sample_file, max_iterations=500, print_generations=False)
    print(f"✅ Solution found: {result['best_solution']}")
    print(f"🎯 Fitness: {result['fitness']}/{result['max_fitness']} ({result['fitness_percentage']:.1f}%)")
    print(f"⏱️  Time: {result['time_elapsed']:.3f} seconds")
    print()
    
    # 2. Using the wrapper class with detailed output
    print("2️⃣  Wrapper Class with Detailed Output")
    print("-" * 40)
    
    wrapper = PBILWrapper()
    result = wrapper.run(
        cnf_file=sample_file,
        pop_size=100,
        learning_rate=0.1,
        negative_learning_rate=0.075,
        mutation_probability=0.02,
        mutation_shift=0.05,
        max_iterations=1000,
        print_generations=True
    )
    wrapper.print_results(result)
    print()
    
    # 3. Parameter comparison
    print("3️⃣  Parameter Comparison")
    print("-" * 40)
    
    parameter_sets = [
        {"name": "Conservative", "pop_size": 50, "learning_rate": 0.05, "mutation_probability": 0.01},
        {"name": "Balanced", "pop_size": 100, "learning_rate": 0.1, "mutation_probability": 0.02},
        {"name": "Aggressive", "pop_size": 200, "learning_rate": 0.2, "mutation_probability": 0.05},
    ]
    
    results = []
    for params in parameter_sets:
        name = params.pop("name")
        print(f"🔬 Testing {name} parameters...")
        
        start_time = time.time()
        result = wrapper.run(cnf_file=sample_file, max_iterations=500, **params)
        end_time = time.time()
        
        results.append({
            "name": name,
            "success": result.get('success', False),
            "fitness": result.get('fitness', 0),
            "max_fitness": result.get('max_fitness', 0),
            "generations": result.get('total_generations', 0),
            "time": end_time - start_time,
            "solution": result.get('best_solution', [])
        })
    
    print("\n📊 Results Summary:")
    print(f"{'Strategy':<12} {'Success':<8} {'Fitness':<10} {'Generations':<12} {'Time (s)':<10}")
    print("-" * 60)
    
    for r in results:
        success_icon = "✅" if r['success'] else "❌"
        fitness_str = f"{r['fitness']}/{r['max_fitness']}"
        print(f"{r['name']:<12} {success_icon:<8} {fitness_str:<10} {r['generations']:<12} {r['time']:.3f}")
    
    print()
    
    # 4. Demonstrate multiple file processing (if more files exist)
    print("4️⃣  Multiple File Processing")
    print("-" * 40)
    
    cnf_files = [f for f in os.listdir('.') if f.endswith('.cnf')]
    if len(cnf_files) > 1:
        print(f"📁 Found {len(cnf_files)} CNF files:")
        
        results = wrapper.run_multiple(cnf_files[:3], max_iterations=200)  # Process up to 3 files
        
        for result in results:
            filename = os.path.basename(result['cnf_file'])
            if 'error' in result:
                print(f"  ❌ {filename}: {result['error']}")
            else:
                success_icon = "✅" if result.get('success') else "⚠️"
                fitness = result.get('fitness', 0)
                max_fitness = result.get('max_fitness', 0)
                print(f"  {success_icon} {filename}: {fitness}/{max_fitness}")
    else:
        print("📁 Only one CNF file found. To test multiple file processing,")
        print("   add more .cnf files to the current directory.")
    
    print()
    
    # 5. Command line interface demonstration
    print("5️⃣  Command Line Interface")
    print("-" * 40)
    print("You can also use the wrapper from the command line:")
    print()
    print("  # Basic usage:")
    print(f"  python evolution_simulation/pbil.py {sample_file}")
    print()
    print("  # With custom parameters:")
    print(f"  python evolution_simulation/pbil.py {sample_file} \\")
    print("    --pop-size 200 --learning-rate 0.15 --max-iterations 2000 --print-generations")
    print()
    
    # 6. Performance note
    print("6️⃣  Performance Notes")
    print("-" * 40)
    print("🚀 This wrapper calls your original C implementation directly,")
    print("   providing the full performance of the native C code while")
    print("   offering a convenient Python interface.")
    print()
    print("🔧 The wrapper handles:")
    print("   • Automatic compilation of C code")
    print("   • Parameter validation")
    print("   • Output parsing and structuring")
    print("   • Error handling and reporting")
    print("   • Memory management (fixed double-free issue)")
    print()
    
    print("✨ Demo completed successfully!")


if __name__ == "__main__":
    main() 