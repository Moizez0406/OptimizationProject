#ifndef SUBJECT_SOLUTION_H  // convention: ALL_CAPS for header guards
#define SUBJECT_SOLUTION_H

#include <algorithm>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>
inline std::random_device rd;
inline std::mt19937 gen(rd());

struct Job {
    int id;
    std::vector<int> times;
};

class Subject_solution {
   private:
    std::vector<Job> permutation;
    int makespan;
    static std::unordered_map<int, Job> job_lookup;

   public:
    Subject_solution(const std::vector<Job>& permutation, int makespan)
        : permutation(permutation), makespan(makespan) {}
    Subject_solution(const std::vector<Job>& permutation);

    static void set_lookup(const std::vector<Job>& subject);
    static Subject_solution from_ids(const std::vector<int>& child_ids);

    // Getters
    std::vector<Job> get_permutation() const { return permutation; }
    int get_makespan() const { return makespan; }
    std::vector<int> get_ids() const;

    // Setters
    void set_makespan(int ms) { makespan = ms; }
    void set_permutation(const std::vector<Job>& perm) { permutation = perm; }

    // Other methods
    void swap_jobs(std::mt19937& gen);
    void shuffle_permutation(std::mt19937& gen) {
        std::shuffle(this->permutation.begin(), this->permutation.end(), gen);
    }
    void compute_makespan() {
        int num_machines = (int)this->permutation[0].times.size();
        std::vector<int> time(num_machines, 0);
        for (const auto& job : this->permutation) {
<<<<<<< HEAD
            for (int i = 0; i < num_machines; i++) {
                if (i == 0) {
                    time[i] += job.times[i];
                } else {
                    time[i] = std::max(time[i], time[i - 1]) + job.times[i];
                }
=======
            time[0] += job.times[0];
            for (int i = 1; i < num_machines; i++) {
                time[i] = std::max(time[i], time[i - 1]) + job.times[i];
>>>>>>> 83805ac (Small fixes across all the project)
            }
        }
        this->makespan = time[num_machines - 1];
    }
    Job pop_front();
    void remove_job(const Job& job);
    void append_job(const Job& job);
    int size() const { return (int)permutation.size(); }
    bool empty() const { return permutation.empty(); }

    Subject_solution copy() const;
    std::string repr() const;

    // operator overloads
    bool operator<(const Subject_solution& other) const {
        return makespan < other.makespan;
    }
    friend std::ostream& operator<<(std::ostream& os,
                                    const Subject_solution& s) {
        os << s.repr();
        return os;
    }
};

#endif  // SUBJECT_SOLUTION_H