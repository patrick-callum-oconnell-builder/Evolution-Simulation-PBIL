//recombined into "dependencies.c" by Patrick O'Connell
//added more functions as well

// Original author of read_cnf and get_fitness: Jack Beckitt-Marshall, 10 Mar 2020

// read-cnf - Reads CNF files and returns Problem structs. 
// get_fitness - Determines fitness of vector candidate solutions w/ respect to maxsat problem
#include "dependencies.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "datatypes.h"

// Takes a filename, and returns a problem struct that efficiently contains the
// problem.
// Parameters: filename - Filename to open.
// Returns: a struct containing the problem.
problem read_cnf(const char* filename) {
    problem prob;
    int current_clause_index = 0;
    FILE* problem_file = fopen(filename, "r");
    char buffer[1024];
    current_clause_index = 0;
    if (problem_file == NULL) {
        printf("Could not open %s\n", filename);
        exit(-1);
    }
    while (fgets(buffer, sizeof buffer, problem_file) != NULL){
        if (buffer[0] == 'c'){
            // Do nothing, skip over comments.
        } else if (buffer[0] == 'p') {
            sscanf(buffer, "p cnf %d %d", &(prob.n_variables), 
                &(prob.n_clauses));
            prob.clauses = (clause*) malloc(sizeof(clause) * prob.n_clauses);
        } else {
            char* token;
            int variables[1024];
            int token_count = 0;
            token = strtok(buffer, " ");
            while (token != NULL) {
                variables[token_count] = atoi(token);
                token_count++;
                token = strtok(NULL, " ");
            }
            token_count -= 1;
            clause* current_clause = prob.clauses + current_clause_index;
            current_clause->literals = (literal*) malloc(
                sizeof(literal) * token_count);
            current_clause->n_literals = token_count;
            for (int i = 0; i < current_clause->n_literals; i++) {
                current_clause->literals[i].var_id = abs(variables[i]);
                if (variables[i] < 0) {
                    current_clause->literals[i].active = 0;
                } else {
                    current_clause->literals[i].active = 1;
                }
            }
            current_clause_index += 1;

        }
    }
    if (feof(problem_file)){
        fclose(problem_file);
        return prob;
    }
    return prob;
}

void free_problem(problem prob) {
    for (int i = 0; i < prob.n_clauses; i++) {
        free(prob.clauses[i].literals);
    }
    free(prob.clauses);
}

int get_fitness(int* vector, problem* prob) {
    int clauses_satisfied = 0;
    for (int i = 0; i < prob->n_clauses; i++) {
        clause current_clause = prob->clauses[i];
        int clause_sum = 0;
        for (int j = 0; j < current_clause.n_literals; j++) {
            if (current_clause.literals[j].active == 1) {
                clause_sum += vector[current_clause.literals[j].var_id - 1];
            } else {
                clause_sum += !vector[current_clause.literals[j].var_id - 1];
            }
        }
        clauses_satisfied += !!clause_sum;
    }
    return clauses_satisfied;
}