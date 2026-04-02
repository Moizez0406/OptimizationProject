#include "Subject_solution.h"

std::unordered_map<int, Job> Subject_solution::job_lookup;

void Subject_solution::set_lookup(const std::vector<Job>& subject) {
    for (const Job& job : subject) {
        job_lookup[job.id] = job;
    }
}

Subject_solution::Subject_solution(const std::vector<Job>& permutation)
    : permutation(permutation) {
    compute_makespan();
}
Subject_solution Subject_solution::from_ids(const std::vector<int>& child_ids) {
    std::vector<Job> perm;
    for (int id : child_ids) {
        perm.push_back(job_lookup[id]);
    }
    return Subject_solution(perm);  // constructor auto-computes makespan
}

Subject_solution Subject_solution::copy() const {
    return Subject_solution(permutation, makespan);
}

std::vector<int> Subject_solution::get_ids() const {
    std::vector<int> result;
    for (const Job& job : permutation) {
        result.push_back(job.id);
    }
    return result;
}

void Subject_solution::swap_jobs(std::mt19937& gen) {
    std::uniform_int_distribution<int> dist(0, (int)permutation.size() - 1);
    int i = dist(gen);
    int j = dist(gen);
    std::swap(permutation[i], permutation[j]);
    compute_makespan();
}

Job Subject_solution::pop_front() {
    Job first = permutation[0];
    permutation.erase(permutation.begin());
    return first;
}
void Subject_solution::remove_job(const Job& job) {
    permutation.erase(
        std::find_if(permutation.begin(), permutation.end(),
                     [&](const Job& j) { return j.id == job.id; }));
}
void Subject_solution::append_job(const Job& job) {
    permutation.push_back(job);
    compute_makespan();  // always stays up to date
}
std::string Subject_solution::repr() const {
    std::string result =
        "Subject_solution(makespan=" + std::to_string(makespan) + ", order=[";
    std::vector<int> id_list = get_ids();
    for (int i = 0; i < (int)id_list.size(); i++) {
        result += std::to_string(id_list[i]);
        if (i < (int)id_list.size() - 1) result += ", ";
    }
    result += "])";
    return result;
}