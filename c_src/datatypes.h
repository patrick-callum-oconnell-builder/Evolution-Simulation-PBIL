#ifndef DATATYPES
#define DATATYPES

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

#endif