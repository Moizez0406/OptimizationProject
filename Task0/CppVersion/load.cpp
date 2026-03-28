#include "load.h"
#include <fstream>
#include <sstream>
#include <stdexcept>

TaillardInstance load_taillard(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + filename);
    }

    // read all non-empty lines
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        // trim whitespace
        size_t start = line.find_first_not_of(" \t\r\n");
        if (start != std::string::npos) {
            lines.push_back(line.substr(start));
        }
    }

    TaillardInstance instance;
    int header_index = -1;

    // --- find header line ---
    for (int idx = 0; idx < (int)lines.size(); idx++) {
        std::istringstream iss(lines[idx]);
        int n_jobs, n_machines, seed, UB, LB;
        if (iss >> n_jobs >> n_machines >> seed >> UB >> LB) {
            // verify nothing left on line — exactly 5 integers
            std::string leftover;
            if (!(iss >> leftover)) {
                instance.n_jobs    = n_jobs;
                instance.n_machines = n_machines;
                instance.UB        = UB;
                instance.LB        = LB;
                header_index       = idx;
                break;
            }
        }
    }

    if (header_index == -1) {
        throw std::runtime_error("Could not find header line in: " + filename);
    }

    // --- find where numeric matrix starts ---
    int data_start = -1;
    for (int idx = header_index + 1; idx < (int)lines.size(); idx++) {
        std::istringstream iss(lines[idx]);
        int val;
        if (iss >> val) {  // line starts with a number
            data_start = idx;
            break;
        }
    }

    if (data_start == -1) {
        throw std::runtime_error("Could not find data matrix in: " + filename);
    }

    // --- read machine data ---
    // machine_data[m][j] = processing time of job j on machine m
    std::vector<std::vector<int>> machine_data;
    for (int m = 0; m < instance.n_machines; m++) {
        std::istringstream iss(lines[data_start + m]);
        std::vector<int> row;
        int val;
        while (iss >> val) {
            row.push_back(val);
        }
        machine_data.push_back(row);
    }

    // --- transpose to job-major and build Job objects ---
    // Python: job = [machine_data[m][j] for m in range(n_machines)]
    for (int j = 0; j < instance.n_jobs; j++) {
        Job job;
        job.id = j;
        for (int m = 0; m < instance.n_machines; m++) {
            job.times.push_back(machine_data[m][j]);
        }
        instance.jobs.push_back(job);
    }

    return instance;
}
