"""
MAXSAT Problem Module

Handles loading and evaluating MAXSAT problems in CNF format.
"""

import numpy as np
from typing import List, Tuple, Optional
from .c_interface import CInterface


class MAXSATProblem:
    """
    MAXSAT problem representation with C backend integration for performance.
    """
    
    def __init__(self, cnf_file: Optional[str] = None):
        """
        Initialize MAXSAT problem.
        
        Args:
            cnf_file: Path to CNF file to load, or None to create empty problem
        """
        self.n_variables = 0
        self.n_clauses = 0
        self.clauses: List[List[int]] = []
        self._c_problem = None
        
        if cnf_file:
            self.load_cnf(cnf_file)
    
    def load_cnf(self, filename: str):
        """
        Load a MAXSAT problem from a CNF file.
        
        Args:
            filename: Path to the CNF file
        """
        print(f"Loading CNF file: {filename}")
        
        # Try to use C backend for loading
        if CInterface.is_available():
            try:
                self._c_problem = CInterface.read_cnf_file(filename)
                # We still need to parse the file in Python to get the structure
                self._parse_cnf_python(filename)
                print(f"✓ Loaded with C backend: {self.n_variables} variables, {self.n_clauses} clauses")
            except Exception as e:
                print(f"C backend failed, using Python fallback: {e}")
                self._parse_cnf_python(filename)
        else:
            self._parse_cnf_python(filename)
    
    def _parse_cnf_python(self, filename: str):
        """
        Parse CNF file using Python (fallback implementation).
        
        Args:
            filename: Path to the CNF file
        """
        self.clauses = []
        
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip comments
                    if line.startswith('c') or not line:
                        continue
                    
                    # Parse problem line
                    if line.startswith('p cnf'):
                        parts = line.split()
                        self.n_variables = int(parts[2])
                        self.n_clauses = int(parts[3])
                        continue
                    
                    # Parse clause
                    literals = [int(x) for x in line.split() if x != '0']
                    if literals:  # Skip empty lines
                        self.clauses.append(literals)
            
            # Verify we got the expected number of clauses
            if len(self.clauses) != self.n_clauses:
                print(f"Warning: Expected {self.n_clauses} clauses, got {len(self.clauses)}")
                self.n_clauses = len(self.clauses)
            
            print(f"✓ Loaded with Python parser: {self.n_variables} variables, {self.n_clauses} clauses")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"CNF file not found: {filename}")
        except Exception as e:
            raise ValueError(f"Error parsing CNF file {filename}: {e}")
    
    def get_fitness(self, solution: np.ndarray) -> int:
        """
        Calculate fitness (number of satisfied clauses) for a solution.
        
        Args:
            solution: Binary solution vector
            
        Returns:
            Number of satisfied clauses
        """
        if CInterface.is_available() and self._c_problem is not None:
            # Use C backend for fitness evaluation
            return CInterface.get_fitness(solution, self._c_problem)
        else:
            # Python fallback
            return self._python_get_fitness(solution)
    
    def _python_get_fitness(self, solution: np.ndarray) -> int:
        """
        Python fallback for fitness evaluation.
        
        Args:
            solution: Binary solution vector
            
        Returns:
            Number of satisfied clauses
        """
        satisfied_clauses = 0
        
        for clause in self.clauses:
            clause_satisfied = False
            
            for literal in clause:
                var_id = abs(literal) - 1  # Convert to 0-based indexing
                var_value = solution[var_id]
                
                # Check if literal is satisfied
                if literal > 0:  # Positive literal
                    if var_value == 1:
                        clause_satisfied = True
                        break
                else:  # Negative literal
                    if var_value == 0:
                        clause_satisfied = True
                        break
            
            if clause_satisfied:
                satisfied_clauses += 1
        
        return satisfied_clauses
    
    def verify_solution(self, solution: np.ndarray) -> Tuple[bool, List[int]]:
        """
        Verify a solution and return details about unsatisfied clauses.
        
        Args:
            solution: Binary solution vector
            
        Returns:
            Tuple of (is_completely_satisfied, list_of_unsatisfied_clause_indices)
        """
        unsatisfied_clauses = []
        
        for clause_idx, clause in enumerate(self.clauses):
            clause_satisfied = False
            
            for literal in clause:
                var_id = abs(literal) - 1  # Convert to 0-based indexing
                var_value = solution[var_id]
                
                # Check if literal is satisfied
                if literal > 0:  # Positive literal
                    if var_value == 1:
                        clause_satisfied = True
                        break
                else:  # Negative literal
                    if var_value == 0:
                        clause_satisfied = True
                        break
            
            if not clause_satisfied:
                unsatisfied_clauses.append(clause_idx)
        
        is_completely_satisfied = len(unsatisfied_clauses) == 0
        return is_completely_satisfied, unsatisfied_clauses
    
    def generate_random_solution(self) -> np.ndarray:
        """Generate a random solution vector."""
        return np.random.randint(0, 2, self.n_variables)
    
    def create_test_problem(self, n_vars: int, n_clauses: int, clause_length: int = 3):
        """
        Create a random test MAXSAT problem.
        
        Args:
            n_vars: Number of variables
            n_clauses: Number of clauses
            clause_length: Length of each clause
        """
        self.n_variables = n_vars
        self.n_clauses = n_clauses
        self.clauses = []
        
        for _ in range(n_clauses):
            clause = []
            variables = np.random.choice(n_vars, clause_length, replace=False) + 1  # 1-based
            
            for var in variables:
                # Randomly negate the literal
                if np.random.random() < 0.5:
                    clause.append(-var)
                else:
                    clause.append(var)
            
            self.clauses.append(clause)
        
        print(f"Created test problem: {n_vars} variables, {n_clauses} clauses")
    
    def save_cnf(self, filename: str):
        """
        Save the problem to a CNF file.
        
        Args:
            filename: Path to save the CNF file
        """
        with open(filename, 'w') as f:
            # Write header
            f.write(f"p cnf {self.n_variables} {self.n_clauses}\n")
            
            # Write clauses
            for clause in self.clauses:
                clause_str = ' '.join(map(str, clause)) + ' 0\n'
                f.write(clause_str)
        
        print(f"Saved CNF file: {filename}")
    
    def get_statistics(self) -> dict:
        """Get problem statistics."""
        if not self.clauses:
            return {'variables': 0, 'clauses': 0, 'avg_clause_length': 0}
        
        clause_lengths = [len(clause) for clause in self.clauses]
        
        return {
            'variables': self.n_variables,
            'clauses': self.n_clauses,
            'avg_clause_length': np.mean(clause_lengths),
            'min_clause_length': np.min(clause_lengths),
            'max_clause_length': np.max(clause_lengths),
            'total_literals': sum(clause_lengths)
        }
    
    def print_problem_info(self):
        """Print detailed problem information."""
        stats = self.get_statistics()
        print(f"MAXSAT Problem Information:")
        print(f"  Variables: {stats['variables']}")
        print(f"  Clauses: {stats['clauses']}")
        print(f"  Average clause length: {stats['avg_clause_length']:.2f}")
        print(f"  Clause length range: {stats['min_clause_length']}-{stats['max_clause_length']}")
        print(f"  Total literals: {stats['total_literals']}")
        
        # Show a few example clauses
        if self.clauses:
            print(f"  Example clauses:")
            for i, clause in enumerate(self.clauses[:3]):
                clause_str = ' ∨ '.join([f"x{abs(lit)}" if lit > 0 else f"¬x{abs(lit)}" for lit in clause])
                print(f"    C{i+1}: {clause_str}")
            if len(self.clauses) > 3:
                print(f"    ... and {len(self.clauses) - 3} more clauses")
    
    def __repr__(self) -> str:
        """String representation of the problem."""
        return f"MAXSATProblem(variables={self.n_variables}, clauses={self.n_clauses})" 