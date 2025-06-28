"""
C Interface Module

Provides Python interface to the PBIL C backend functions.
"""

import numpy as np
from typing import List, Tuple, Optional
try:
    from _pbil_c import lib, ffi
except ImportError:
    # Fallback for development when C extension isn't built yet
    print("Warning: C extension not available. Run 'pip install -e .' to build it.")
    lib = None
    ffi = None


class CInterface:
    """Interface to PBIL C backend functions."""
    
    @staticmethod
    def is_available() -> bool:
        """Check if C extension is available."""
        return lib is not None and ffi is not None
    
    @staticmethod
    def read_cnf_file(filename: str):
        """
        Read a CNF file and return a problem structure.
        
        Args:
            filename: Path to the CNF file
            
        Returns:
            C problem structure pointer or None if extension not available
        """
        if not CInterface.is_available():
            return None
        
        filename_bytes = filename.encode('utf-8')
        return lib.read_cnf(filename_bytes)
    
    @staticmethod
    def get_fitness(vector: np.ndarray, problem_ptr) -> int:
        """
        Calculate fitness of a solution vector for a MAXSAT problem.
        
        Args:
            vector: Binary solution vector
            problem_ptr: C problem structure pointer
            
        Returns:
            Fitness value (number of satisfied clauses)
        """
        if not CInterface.is_available() or problem_ptr is None:
            # Fallback Python implementation would go here
            return 0
        
        # Convert numpy array to C array
        vector_len = len(vector)
        c_vector = ffi.new("int[]", vector_len)
        for i in range(vector_len):
            c_vector[i] = int(vector[i])
        
        return lib.get_fitness(c_vector, problem_ptr)
    
    @staticmethod
    def generate_population(prob_vector: np.ndarray, pop_size: int) -> np.ndarray:
        """
        Generate a population from a probability vector using C implementation.
        
        Args:
            prob_vector: Probability vector for generating individuals
            pop_size: Number of individuals to generate
            
        Returns:
            2D numpy array representing the population
        """
        vector_len = len(prob_vector)
        
        if not CInterface.is_available():
            # Fallback Python implementation
            return CInterface._python_generate_population(prob_vector, pop_size)
        
        # Create C arrays
        c_prob_vector = ffi.new("double[]", vector_len)
        for i in range(vector_len):
            c_prob_vector[i] = prob_vector[i]
        
        # Create population array
        c_population = ffi.new("int*[]", pop_size)
        for i in range(pop_size):
            c_population[i] = ffi.new("int[]", vector_len)
        
        # Generate population
        lib.generate_population(c_population, c_prob_vector, pop_size, vector_len)
        
        # Convert back to numpy array
        population = np.zeros((pop_size, vector_len), dtype=int)
        for i in range(pop_size):
            for j in range(vector_len):
                population[i, j] = c_population[i][j]
        
        return population
    
    @staticmethod
    def update_probability_vector(prob_vector: np.ndarray, best_vector: np.ndarray, 
                                  worst_vector: np.ndarray, lr: float, negative_lr: float) -> np.ndarray:
        """
        Update probability vector based on best and worst individuals.
        
        Args:
            prob_vector: Current probability vector
            best_vector: Best individual from population
            worst_vector: Worst individual from population
            lr: Learning rate
            negative_lr: Negative learning rate
            
        Returns:
            Updated probability vector
        """
        vector_len = len(prob_vector)
        
        if not CInterface.is_available():
            # Fallback Python implementation
            return CInterface._python_update_prob_vector(prob_vector, best_vector, worst_vector, lr, negative_lr)
        
        # Create C arrays
        c_prob_vector = ffi.new("double[]", vector_len)
        c_best_vector = ffi.new("int[]", vector_len)
        c_worst_vector = ffi.new("int[]", vector_len)
        
        for i in range(vector_len):
            c_prob_vector[i] = prob_vector[i]
            c_best_vector[i] = int(best_vector[i])
            c_worst_vector[i] = int(worst_vector[i])
        
        # Update probability vector
        updated_ptr = lib.update_prob_vector(c_prob_vector, vector_len, c_best_vector, c_worst_vector, lr, negative_lr)
        
        # Convert back to numpy array
        updated_vector = np.zeros(vector_len)
        for i in range(vector_len):
            updated_vector[i] = updated_ptr[i]
        
        return updated_vector
    
    @staticmethod
    def find_best_individual(population: np.ndarray, problem_ptr) -> Tuple[np.ndarray, int]:
        """
        Find the best individual in a population.
        
        Args:
            population: 2D array representing the population
            problem_ptr: C problem structure pointer
            
        Returns:
            Tuple of (best_individual, best_fitness)
        """
        if not CInterface.is_available() or problem_ptr is None:
            # Fallback Python implementation
            return CInterface._python_find_best(population, problem_ptr)
        
        pop_size, vector_len = population.shape
        
        # Create C population array
        c_population = ffi.new("int*[]", pop_size)
        for i in range(pop_size):
            c_population[i] = ffi.new("int[]", vector_len)
            for j in range(vector_len):
                c_population[i][j] = int(population[i, j])
        
        # Find best individual
        best_ptr = lib.findBest(c_population, pop_size, vector_len, problem_ptr)
        
        # Convert back to numpy array
        best_individual = np.zeros(vector_len, dtype=int)
        for i in range(vector_len):
            best_individual[i] = best_ptr[i]
        
        # Calculate fitness
        best_fitness = CInterface.get_fitness(best_individual, problem_ptr)
        
        return best_individual, best_fitness
    
    @staticmethod
    def mutate_probability_vector(prob_vector: np.ndarray, mut_probability: float, mut_shift: float) -> np.ndarray:
        """
        Apply mutation to the probability vector.
        
        Args:
            prob_vector: Probability vector to mutate
            mut_probability: Probability of mutation for each bit
            mut_shift: Amount of mutation shift
            
        Returns:
            Mutated probability vector
        """
        if not CInterface.is_available():
            # Fallback Python implementation
            return CInterface._python_mutate(prob_vector, mut_probability, mut_shift)
        
        vector_len = len(prob_vector)
        
        # Create C array
        c_prob_vector = ffi.new("double[]", vector_len)
        for i in range(vector_len):
            c_prob_vector[i] = prob_vector[i]
        
        # Apply mutation
        mutated_ptr = lib.mutate(c_prob_vector, mut_probability, mut_shift)
        
        # Convert back to numpy array
        mutated_vector = np.zeros(vector_len)
        for i in range(vector_len):
            mutated_vector[i] = mutated_ptr[i]
        
        return mutated_vector
    
    # Fallback Python implementations
    @staticmethod
    def _python_generate_population(prob_vector: np.ndarray, pop_size: int) -> np.ndarray:
        """Python fallback for population generation."""
        vector_len = len(prob_vector)
        population = np.random.rand(pop_size, vector_len) <= prob_vector
        return population.astype(int)
    
    @staticmethod
    def _python_update_prob_vector(prob_vector: np.ndarray, best_vector: np.ndarray, 
                                   worst_vector: np.ndarray, lr: float, negative_lr: float) -> np.ndarray:
        """Python fallback for probability vector update."""
        # Update towards best vector
        updated = prob_vector * (1.0 - lr) + best_vector * lr
        
        # Update away from worst vector (where best != worst)
        mask = (best_vector != worst_vector)
        updated[mask] = updated[mask] * (1.0 - negative_lr) + best_vector[mask] * negative_lr
        
        return updated
    
    @staticmethod
    def _python_find_best(population: np.ndarray, problem_ptr) -> Tuple[np.ndarray, int]:
        """Python fallback for finding best individual."""
        if problem_ptr is None:
            # Simple random fitness for testing
            fitnesses = np.random.randint(0, 100, len(population))
        else:
            fitnesses = [CInterface.get_fitness(ind, problem_ptr) for ind in population]
        
        best_idx = np.argmax(fitnesses)
        return population[best_idx], fitnesses[best_idx]
    
    @staticmethod
    def _python_mutate(prob_vector: np.ndarray, mut_probability: float, mut_shift: float) -> np.ndarray:
        """Python fallback for mutation."""
        vector_len = len(prob_vector)
        mutated = prob_vector.copy()
        
        for i in range(vector_len):
            if np.random.random() <= mut_probability:
                direction = np.random.randint(0, 2)  # 0 or 1
                mutated[i] = mutated[i] * (1.0 - mut_shift) + direction * mut_shift
        
        return np.clip(mutated, 0.0, 1.0) 