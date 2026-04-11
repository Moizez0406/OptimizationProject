#ifndef LOAD_H
#define LOAD_H

#include <string>

#include "Subject_solution.h"

struct TaillardInstance {
    int n_jobs;
    int n_machines;
    int UB;
    int LB;
    std::vector<Job> jobs;
};

TaillardInstance load_taillard(const std::string& filename);

#endif  // LOAD_H
