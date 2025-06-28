#ifndef dependencies

#include <stdlib.h>
#include <stdio.h>
#include "datatypes.h"

// Gets the fitness of a problem!
int get_fitness(int* vector, problem* prob);
problem read_cnf(const char* filename);
void free_problem(problem prob);

#endif