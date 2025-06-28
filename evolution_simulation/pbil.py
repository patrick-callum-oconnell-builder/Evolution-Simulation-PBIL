"""
PBIL (Population Based Incremental Learning) Module

Main PBIL algorithm implementation with C backend integration for performance.
"""

import numpy as np
from typing import Tuple, Optional, List
from .c_interface import CInterface
from .maxsat_problem import MAXSATProblem


class PBIL:
    """
    Population Based Incremental Learning algorithm for solving MAXSAT problems.
    Uses C backend for performance-critical operations with Python fallback.
    """
    
    def __init__(self, 
                 problem: MAXSATProblem,
                 pop_size: int = 100,
                 learning_rate: float = 0.1,
                 negative_learning_rate: float = 0.075,
                 mutation_probability: float = 0.02,
                 mutation_shift: float = 0.05):
        """
        Initialize PBIL algorithm.
        
        Args:
            problem: MAXSAT problem to solve
            pop_size: Population size
            learning_rate: Learning rate for updating probability vector
            negative_learning_rate: Negative learning rate
            mutation_probability: Probability of mutation for each bit
            mutation_shift: Amount of mutation shift
        """
        self.problem = problem
        self.pop_size = pop_size
        self.learning_rate = learning_rate
        self.negative_learning_rate = negative_learning_rate
        self.mutation_probability = mutation_probability
        self.mutation_shift = mutation_shift
        
        # Initialize probability vector with 0.5 for all bits
        self.prob_vector = np.full(problem.n_variables, 0.5)
        
        # Track best solution found
        self.best_solution: Optional[np.ndarray] = None
        self.best_fitness: int = 0
        self.best_generation: int = 0
        
        # Statistics
        self.generation = 0
        self.fitness_history: List[Tuple[int, int, float]] = []  # (generation, best_fitness, avg_fitness)
        
        print(f"PBIL initialized for {problem.n_variables} variables, {problem.n_clauses} clauses")
        if CInterface.is_available():
            print("✓ Using high-performance C backend")
        else:
            print("⚠ Using Python fallback (install with 'pip install -e .' for C backend)")
    
    def run(self, max_generations: int = 1000, target_fitness: Optional[int] = None, verbose: bool = True) -> Tuple[np.ndarray, int]:
        """
        Run the PBIL algorithm.
        
        Args:
            max_generations: Maximum number of generations
            target_fitness: Stop if this fitness is reached (default: all clauses satisfied)
            verbose: Print progress information
            
        Returns:
            Tuple of (best_solution, best_fitness)
        """
        if target_fitness is None:
            target_fitness = self.problem.n_clauses  # All clauses satisfied
        
        print(f"Running PBIL for up to {max_generations} generations...")
        print(f"Target fitness: {target_fitness}/{self.problem.n_clauses} clauses")
        
        for gen in range(max_generations):
            self.generation = gen
            
            # Generate population from probability vector
            population = CInterface.generate_population(self.prob_vector, self.pop_size)
            
            # Evaluate fitness for all individuals
            fitnesses = self._evaluate_population(population)
            
            # Find best and worst individuals
            best_idx = np.argmax(fitnesses)
            worst_idx = np.argmin(fitnesses)
            
            best_individual = population[best_idx]
            worst_individual = population[worst_idx]
            best_gen_fitness = fitnesses[best_idx]
            
            # Update global best if we found a better solution
            if best_gen_fitness > self.best_fitness:
                self.best_solution = best_individual.copy()
                self.best_fitness = best_gen_fitness
                self.best_generation = gen
            
            # Record statistics
            avg_fitness = np.mean(fitnesses)
            self.fitness_history.append((gen, self.best_fitness, avg_fitness))
            
            # Print progress
            if verbose and (gen % 100 == 0 or best_gen_fitness >= target_fitness):
                print(f"Generation {gen}: Best={self.best_fitness}/{self.problem.n_clauses}, "
                      f"Current={best_gen_fitness}, Avg={avg_fitness:.2f}")
            
            # Check termination condition
            if self.best_fitness >= target_fitness:
                print(f"✓ Target fitness reached at generation {gen}!")
                break
            
            # Update probability vector (except on first generation)
            if gen > 0:
                self.prob_vector = CInterface.update_probability_vector(
                    self.prob_vector, best_individual, worst_individual,
                    self.learning_rate, self.negative_learning_rate
                )
                
                # Apply mutation
                self.prob_vector = CInterface.mutate_probability_vector(
                    self.prob_vector, self.mutation_probability, self.mutation_shift
                )
                
                # Ensure probabilities stay in valid range
                self.prob_vector = np.clip(self.prob_vector, 0.0, 1.0)
        
        print(f"PBIL completed after {self.generation + 1} generations")
        print(f"Best solution found at generation {self.best_generation}: {self.best_fitness}/{self.problem.n_clauses} clauses satisfied")
        
        return self.best_solution, self.best_fitness
    
    def _evaluate_population(self, population: np.ndarray) -> np.ndarray:
        """
        Evaluate fitness for all individuals in the population.
        
        Args:
            population: 2D array of individuals
            
        Returns:
            Array of fitness values
        """
        fitnesses = np.zeros(len(population), dtype=int)
        
        for i, individual in enumerate(population):
            fitnesses[i] = self.problem.get_fitness(individual)
        
        return fitnesses
    
    def get_statistics(self) -> dict:
        """Get current algorithm statistics."""
        return {
            'generation': self.generation,
            'best_fitness': self.best_fitness,
            'best_generation': self.best_generation,
            'target_fitness': self.problem.n_clauses,
            'success_rate': self.best_fitness / self.problem.n_clauses if self.problem.n_clauses > 0 else 0,
            'prob_vector_entropy': self._calculate_entropy(),
            'prob_vector_mean': np.mean(self.prob_vector),
            'prob_vector_std': np.std(self.prob_vector)
        }
    
    def _calculate_entropy(self) -> float:
        """Calculate entropy of the probability vector (measure of diversity)."""
        # Avoid log(0) by adding small epsilon
        epsilon = 1e-10
        p = np.clip(self.prob_vector, epsilon, 1 - epsilon)
        entropy = -np.sum(p * np.log2(p) + (1 - p) * np.log2(1 - p))
        return entropy / len(p)  # Normalize by vector length
    
    def visualize_progress(self):
        """Visualize the algorithm's progress."""
        try:
            import matplotlib.pyplot as plt
            
            if not self.fitness_history:
                print("No fitness history to visualize")
                return
            
            generations, best_fitnesses, avg_fitnesses = zip(*self.fitness_history)
            
            plt.figure(figsize=(12, 8))
            
            # Plot fitness progress
            plt.subplot(2, 2, 1)
            plt.plot(generations, best_fitnesses, 'b-', label='Best Fitness', linewidth=2)
            plt.plot(generations, avg_fitnesses, 'r--', label='Average Fitness', alpha=0.7)
            plt.axhline(y=self.problem.n_clauses, color='g', linestyle=':', label='Target Fitness')
            plt.xlabel('Generation')
            plt.ylabel('Fitness (Clauses Satisfied)')
            plt.title('PBIL Fitness Progress')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Plot probability vector histogram
            plt.subplot(2, 2, 2)
            plt.hist(self.prob_vector, bins=20, alpha=0.7, edgecolor='black')
            plt.xlabel('Probability Value')
            plt.ylabel('Frequency')
            plt.title('Probability Vector Distribution')
            plt.grid(True, alpha=0.3)
            
            # Plot probability vector over time (if we have enough data)
            if len(self.fitness_history) > 10:
                plt.subplot(2, 1, 2)
                # Sample some probability values to show evolution
                sample_indices = np.linspace(0, len(self.prob_vector) - 1, min(10, len(self.prob_vector)), dtype=int)
                for i in sample_indices:
                    # This would require storing prob_vector history - simplified for now
                    plt.axhline(y=self.prob_vector[i], alpha=0.5, label=f'Var {i}' if i < 5 else '')
                plt.xlabel('Variable Index')
                plt.ylabel('Probability')
                plt.title('Current Probability Vector')
                plt.grid(True, alpha=0.3)
                if len(sample_indices) <= 5:
                    plt.legend()
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("Matplotlib not available. Install with: pip install matplotlib")
    
    def get_solution_string(self) -> str:
        """Get the best solution as a readable string."""
        if self.best_solution is None:
            return "No solution found yet"
        
        return ''.join(map(str, self.best_solution.astype(int)))
    
    def verify_solution(self) -> Tuple[bool, List[int]]:
        """
        Verify the best solution and return unsatisfied clauses.
        
        Returns:
            Tuple of (is_valid, list_of_unsatisfied_clause_indices)
        """
        if self.best_solution is None:
            return False, []
        
        return self.problem.verify_solution(self.best_solution)
    
    def __repr__(self) -> str:
        """String representation of the PBIL instance."""
        stats = self.get_statistics()
        return (f"PBIL(generation={stats['generation']}, "
                f"best_fitness={stats['best_fitness']}/{stats['target_fitness']}, "
                f"success_rate={stats['success_rate']:.2%})") 