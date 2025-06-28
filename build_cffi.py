import cffi
import os

ffibuilder = cffi.FFI()

# Define the C API that will be exposed to Python - PBIL structures and functions
ffibuilder.cdef("""
    // PBIL data structures
    typedef struct s_literal {
        int var_id;
        int active;
    } literal;

    typedef struct s_clause {
        literal* literals;
        int n_literals;
    } clause;

    typedef struct s_problem {
        clause* clauses;
        int n_clauses;
        int n_variables;
    } problem;
    
    // Core PBIL functions
    int** generate_population(int** current_population, double* prob_vector, int pop_size, int length);
    double* update_prob_vector(double* prob_vector, int length, int* best_vector, int* worst_vector, double lr, double negative_lr);
    int* findBest(int** current_population, int pop_size, int length, problem* prob);
    int* findWorst(int** current_population, int pop_size, int length, int max_fitness, problem* prob);
    double* mutate(double* prob_vector, double mut_probability, double mut_shift);
    
    // Problem handling functions
    problem read_cnf(const char* filename);
    int get_fitness(int* vector, problem* prob);
    void free_problem(problem prob);
    
    // Memory management helpers
    void* malloc(size_t size);
    void free(void* ptr);
""")

# Get all .c files from c_src directory (except the main file)
c_files = []
c_src_dir = "c_src"
if os.path.exists(c_src_dir):
    all_files = [f for f in os.listdir(c_src_dir) if f.endswith('.c')]
    # Exclude the main driver file since we only want the library functions
    c_files = [os.path.join(c_src_dir, f) for f in all_files if f != 'pbil_c.c']

# Include necessary headers and source files
source_files = []
if c_files:
    source_files = c_files
else:
    # Fallback if no files found
    source_files = ['c_src/c_helper_functions.c', 'c_src/dependencies.c']

ffibuilder.set_source("_pbil_c",
    """
    #include "datatypes.h"
    #include "dependencies.h"
    #include "helper_pbil.h"
    """,
    sources=source_files,
    libraries=['m'],  # Link math library
    include_dirs=['c_src'],  # Include directory for headers
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True) 