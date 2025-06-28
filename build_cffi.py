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
    
    // Main PBIL function - wrapper around the original main
    int run_pbil(int pop_size, double lr, double negative_lr, double mut_probability, 
                 double mut_shift, int max_iterations, const char* file_name, int print_generations);
    
    // Memory management helpers
    void* malloc(size_t size);
    void free(void* ptr);
""")

# Get all .c files from c_src directory (except the main file)
c_files = []
c_src_dir = "c_src"
if os.path.exists(c_src_dir):
    all_files = [f for f in os.listdir(c_src_dir) if f.endswith('.c')]
    # Include helper functions and dependencies, but we'll need to modify pbil_c.c
    c_files = [os.path.join(c_src_dir, f) for f in all_files if f != 'pbil_c.c']

# Include necessary headers and create wrapper function
source_files = []
if c_files:
    source_files = c_files
else:
    # Fallback if no files found
    source_files = ['c_src/c_helper_functions.c', 'c_src/dependencies.c']

ffibuilder.set_source("_pbil_c",
    """
    #include <stdio.h>
    #include <stdlib.h>
    #include <stdbool.h>
    #include <string.h>
    #include <time.h>
    #include "datatypes.h"
    #include "dependencies.h"
    #include "helper_pbil.h"
    
    // Wrapper function that calls the PBIL algorithm logic (extracted from main)
    int run_pbil(int pop_size, double lr, double negative_lr, double mut_probability, 
                 double mut_shift, int max_iterations, const char* file_name, int print_generations) {
        
        // Redirect stdout to capture output (optional)
        // We'll let it print normally for now
        
        int epoch = 100;
        clock_t start_time = clock();
        
        problem maxsat_problem = read_cnf(file_name);
        int max_fitness = maxsat_problem.n_clauses;
        int vector_len = maxsat_problem.n_variables;
        bool max_fitness_reached = false;
        
        // Initialize probability vector
        double* prob_vector = (double*) malloc(vector_len * sizeof(double));
        for (int i = 0; i < vector_len; i++) {
            prob_vector[i] = 0.5;
        }
        
        // Initialize vectors for best and worst individuals
        int* best_vector = (int*) malloc(vector_len * sizeof(int));
        int* worst_vector = (int*) malloc(vector_len * sizeof(int));
        int* best_global_vector = (int*) malloc((vector_len + 1) * sizeof(int));
        
        for (int i = 0; i < vector_len; i++) {
            best_vector[i] = 0;
            worst_vector[i] = 0;
            best_global_vector[i] = 0;
        }
        
        int best_global_fitness = get_fitness(best_vector, &maxsat_problem);
        
        // Initialize population
        int** current_population = (int**) malloc(pop_size * sizeof(int*));
        for (int i = 0; i < pop_size; i++) {
            current_population[i] = (int*) malloc(vector_len * sizeof(int));
        }
        
        printf("\\nBeginning iterative process...\\n");
        
        // Main PBIL loop
        int iteration = 0;
        while ((iteration < max_iterations) && !max_fitness_reached) {
            
            // Print progress
            if (print_generations == 1 && iteration % epoch == 0) {
                printf("Generation: %d\\n", iteration);
                printf("Best individual: <");
                for (int i = 0; i < vector_len; i++) {
                    printf("%d ", best_vector[i]);
                }
                printf(">\\n");
                printf("Probability Vector: <");
                for (int i = 0; i < vector_len; i++) {
                    printf("%.3f ", prob_vector[i]);
                }
                printf(">\\n\\n");
            }
            
            // Update probability vector (skip first iteration)
            if (iteration > 0) {
                prob_vector = update_prob_vector(prob_vector, vector_len, best_vector, worst_vector, lr, negative_lr);
                prob_vector = mutate(prob_vector, mut_probability, mut_shift);
            }
            
            // Generate new population
            current_population = generate_population(current_population, prob_vector, pop_size, vector_len);
            
            // Find best and worst
            best_vector = findBest(current_population, pop_size, vector_len, &maxsat_problem);
            int best_fitness = get_fitness(best_vector, &maxsat_problem);
            
            if (best_fitness == max_fitness) {
                printf("Reached max fitness w/ candidate solution!\\n");
                max_fitness_reached = true;
            }
            
            // Update global best
            if (best_fitness > best_global_fitness) {
                best_global_fitness = best_fitness;
                best_global_vector[0] = iteration;
                for (int i = 1; i < (vector_len + 1); i++) {
                    best_global_vector[i] = best_vector[i - 1];
                }
            }
            
            worst_vector = findWorst(current_population, pop_size, vector_len, max_fitness, &maxsat_problem);
            iteration++;
        }
        
        double time_elapsed = ((double) (clock() - start_time)) / CLOCKS_PER_SEC;
        
        // Print final results
        printf("Algorithm completed successfully.\\nTime elapsed: %.2f seconds\\n\\n", time_elapsed);
        printf("Results for problem %s (%d variables, %d clauses):\\n", file_name, maxsat_problem.n_variables, maxsat_problem.n_clauses);
        printf("----------------------------------------------\\n");
        printf("Total generations created: %d\\n", iteration);
        printf("Best candidate solution found: <");
        for (int i = 1; i < (vector_len + 1); i++) {
            printf("%d ", best_global_vector[i]);
        }
        printf(">\\n");
        printf("at generation %d\\n", best_global_vector[0]);
        printf("Candidate fitness: satisfied %d of %d clauses ", best_global_fitness, max_fitness);
        printf("(%.02f%% fit)\\n", (((double) best_global_fitness) / ((double) max_fitness)) * 100);
        printf("----------------------------------------------\\n");
        
        // Cleanup
        free(prob_vector);
        free(best_vector);
        free(worst_vector);
        free(best_global_vector);
        for (int i = 0; i < pop_size; i++) {
            free(current_population[i]);
        }
        free(current_population);
        free_problem(maxsat_problem);
        
        return best_global_fitness;
    }
    """,
    sources=source_files,
    libraries=['m'],  # Link math library
    include_dirs=['c_src'],  # Include directory for headers
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True) 