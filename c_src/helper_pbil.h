#ifndef HELPER_PBIL_H
#define HELPER_PBIL_H

#include "datatypes.h"

// Function declarations for PBIL helper functions

// Generate population from probability vector
int** generate_population(int** current_population, double* prob_vector, int pop_size, int length);

// Update probability vector based on best and worst individuals
double* update_prob_vector(double* prob_vector, int length, int* best_vector, int* worst_vector, double lr, double negative_lr);

// Find best individual in population
int* findBest(int** current_population, int pop_size, int length, problem* prob);

// Find worst individual in population
int* findWorst(int** current_population, int pop_size, int length, int max_fitness, problem* prob);

// Mutate probability vector
double* mutate(double* prob_vector, double mut_probability, double mut_shift);

#endif 