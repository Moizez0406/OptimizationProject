#ifndef LOAD_H
#define LOAD_H

#include "Subject_solution.h"
#include <string>

struct TaillardInstance {
    int n_jobs;
    int n_machines;
    int UB;
    int LB;
    std::vector<Job> jobs;  // already structured as Job namedtuples
};

TaillardInstance load_taillard(const std::string& filename);

#endif // LOAD_H
