#!/usr/bin/env python3
"""
Main Example Script

Demonstrates the PBIL algorithm with C backend integration for solving MAXSAT problems.
"""

import time
import numpy as np
from evolution_simulation import PBIL, MAXSATProblem, CInterface


def main():
    """Main PBIL demonstration."""
    print("PBIL (Population Based Incremental Learning) with C Backend")
    print("=" * 60)
    
    # Check if C extension is available
    if CInterface.is_available():
        print("✓ C extension loaded successfully - high performance mode enabled")
    else:
        print("⚠ C extension not available - running in Python fallback mode")
        print("  To enable C backend, run: pip install -e .")
    
    print()
    
    # Example 1: Create and solve a test problem
    print("Example 1: Random Test Problem")
    print("-" * 30)
    
    # Create a test MAXSAT problem
    problem = MAXSATProblem()
    problem.create_test_problem(n_vars=20, n_clauses=50, clause_length=3)
    problem.print_problem_info()
    
    # Create PBIL solver
    pbil = PBIL(
        problem=problem,
        pop_size=50,
        learning_rate=0.1,
        negative_learning_rate=0.075,
        mutation_probability=0.02,
        mutation_shift=0.05
    )
    
    # Run the algorithm
    print("\nRunning PBIL...")
    start_time = time.time()
    
    solution, fitness = pbil.run(max_generations=500, verbose=True)
    
    end_time = time.time()
    runtime = end_time - start_time
    
    # Show results
    print(f"\nResults:")
    print(f"Runtime: {runtime:.3f} seconds")
    print(f"Best solution: {pbil.get_solution_string()}")
    print(f"Fitness: {fitness}/{problem.n_clauses} clauses satisfied ({fitness/problem.n_clauses*100:.1f}%)")
    
    # Verify solution
    is_valid, unsatisfied = pbil.verify_solution()
    if is_valid:
        print("✓ Solution satisfies all clauses!")
    else:
        print(f"⚠ Solution leaves {len(unsatisfied)} clauses unsatisfied")
    
    # Show statistics
    stats = pbil.get_statistics()
    print(f"\nAlgorithm Statistics:")
    print(f"  Final generation: {stats['generation']}")
    print(f"  Best found at generation: {stats['best_generation']}")
    print(f"  Success rate: {stats['success_rate']:.1%}")
    print(f"  Probability vector entropy: {stats['prob_vector_entropy']:.3f}")
    
    # Optional visualization
    try:
        print("\nGenerating visualization...")
        pbil.visualize_progress()
    except Exception as e:
        print(f"Visualization not available: {e}")
    
    print("\n" + "="*60)


def load_cnf_example():
    """Example of loading and solving a CNF file."""
    print("Example 2: Loading CNF File")
    print("-" * 30)
    
    # Create a sample CNF file first
    sample_cnf = "sample_problem.cnf"
    create_sample_cnf(sample_cnf)
    
    try:
        # Load the CNF file
        problem = MAXSATProblem(sample_cnf)
        problem.print_problem_info()
        
        # Solve it
        pbil = PBIL(problem, pop_size=30)
        solution, fitness = pbil.run(max_generations=200, verbose=False)
        
        print(f"Solution: {pbil.get_solution_string()}")
        print(f"Satisfied: {fitness}/{problem.n_clauses} clauses")
        
    except Exception as e:
        print(f"Error loading CNF file: {e}")


def create_sample_cnf(filename: str):
    """Create a sample CNF file for demonstration."""
    # Simple 3-SAT problem: (x1 ∨ ¬x2 ∨ x3) ∧ (¬x1 ∨ x2 ∨ ¬x3) ∧ (x1 ∨ x2 ∨ x3)
    with open(filename, 'w') as f:
        f.write("c Sample 3-SAT problem\n")
        f.write("c Variables: x1, x2, x3\n")
        f.write("p cnf 3 3\n")
        f.write("1 -2 3 0\n")  # (x1 ∨ ¬x2 ∨ x3)
        f.write("-1 2 -3 0\n") # (¬x1 ∨ x2 ∨ ¬x3)
        f.write("1 2 3 0\n")   # (x1 ∨ x2 ∨ x3)
    
    print(f"Created sample CNF file: {filename}")


def performance_comparison():
    """Compare performance between different problem sizes."""
    print("Example 3: Performance Comparison")
    print("-" * 30)
    
    problem_sizes = [
        (10, 25),   # Small
        (20, 50),   # Medium
        (30, 100),  # Large
    ]
    
    for n_vars, n_clauses in problem_sizes:
        print(f"\nTesting problem: {n_vars} variables, {n_clauses} clauses")
        
        # Create problem
        problem = MAXSATProblem()
        problem.create_test_problem(n_vars, n_clauses)
        
        # Run PBIL
        pbil = PBIL(problem, pop_size=50)
        
        start_time = time.time()
        solution, fitness = pbil.run(max_generations=200, verbose=False)
        runtime = time.time() - start_time
        
        success_rate = fitness / problem.n_clauses
        print(f"  Runtime: {runtime:.3f}s")
        print(f"  Result: {fitness}/{n_clauses} clauses ({success_rate:.1%})")
        print(f"  Performance: {pbil.generation * pbil.pop_size / runtime:.0f} evaluations/sec")


def parameter_tuning_example():
    """Example of testing different PBIL parameters."""
    print("Example 4: Parameter Tuning")
    print("-" * 30)
    
    # Create a fixed test problem
    problem = MAXSATProblem()
    problem.create_test_problem(15, 40)
    
    # Test different parameter combinations
    parameter_sets = [
        {"learning_rate": 0.05, "negative_learning_rate": 0.025, "name": "Conservative"},
        {"learning_rate": 0.1, "negative_learning_rate": 0.075, "name": "Standard"},
        {"learning_rate": 0.2, "negative_learning_rate": 0.15, "name": "Aggressive"},
    ]
    
    results = []
    
    for params in parameter_sets:
        name = params.pop("name")
        print(f"\nTesting {name} parameters: {params}")
        
        pbil = PBIL(problem, pop_size=50, **params)
        
        start_time = time.time()
        solution, fitness = pbil.run(max_generations=300, verbose=False)
        runtime = time.time() - start_time
        
        success_rate = fitness / problem.n_clauses
        results.append((name, fitness, success_rate, runtime, pbil.generation))
        
        print(f"  Result: {fitness}/{problem.n_clauses} ({success_rate:.1%}) in {runtime:.3f}s")
    
    # Summary
    print(f"\nParameter Comparison Summary:")
    print(f"{'Method':<12} {'Fitness':<8} {'Success':<8} {'Time':<8} {'Gens':<8}")
    print("-" * 50)
    for name, fitness, success, runtime, gens in results:
        print(f"{name:<12} {fitness:<8} {success:<7.1%} {runtime:<7.3f}s {gens:<8}")


if __name__ == "__main__":
    main()
    
    # Uncomment to run additional examples
    print("\n")
    load_cnf_example()
    
    print("\n")
    performance_comparison()
    
    print("\n")
    parameter_tuning_example()
    
    print("\nAll examples completed!") 