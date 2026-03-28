#include <iostream>

#include "Subject_solution.h"
#include "algo.h"
#include "load.h"

int main() {
    TaillardInstance inst = load_taillard("../tai100_10_0.fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution sol(inst.jobs);

    const int RUNS = 20;

    int sum_rs = 0, sum_sa = 0, sum_ga = 0;
    int sumsq_rs = 0, sumsq_sa = 0, sumsq_ga = 0;

    Subject_solution rs = randomSearch(sol);
    Subject_solution sa = simulatedAnnealing(sol);
    Subject_solution ga = genetic(sol);
    Subject_solution gr = greedy(sol);

    Subject_solution worst_rs = rs;
    Subject_solution worst_sa = sa;
    Subject_solution worst_ga = ga;

    for (int i = 0; i < RUNS; i++) {
        Subject_solution curr_rs = randomSearch(sol);
        Subject_solution curr_sa = simulatedAnnealing(sol);
        Subject_solution curr_ga = genetic(sol);

        int m_rs = curr_rs.get_makespan();
        int m_sa = curr_sa.get_makespan();
        int m_ga = curr_ga.get_makespan();

        // ---- accumulate ----
        sum_rs += m_rs;
        sum_sa += m_sa;
        sum_ga += m_ga;

        sumsq_rs += m_rs * m_rs;
        sumsq_sa += m_sa * m_sa;
        sumsq_ga += m_ga * m_ga;

        // ---- BEST ----
        if (m_rs < rs.get_makespan()) rs = curr_rs.copy();
        if (m_sa < sa.get_makespan()) sa = curr_sa.copy();
        if (m_ga < ga.get_makespan()) ga = curr_ga;

        // ---- WORST ----
        if (m_rs > worst_rs.get_makespan()) worst_rs = curr_rs.copy();
        if (m_sa > worst_sa.get_makespan()) worst_sa = curr_sa.copy();
        if (m_ga > worst_ga.get_makespan()) worst_ga = curr_ga;
    }
    double avg_rs = (double)sum_rs / RUNS;
    double avg_sa = (double)sum_sa / RUNS;
    double avg_ga = (double)sum_ga / RUNS;

    double std_rs = sqrt((double)sumsq_rs / RUNS - avg_rs * avg_rs);
    double std_sa = sqrt((double)sumsq_sa / RUNS - avg_sa * avg_sa);
    double std_ga = sqrt((double)sumsq_ga / RUNS - avg_ga * avg_ga);
    std::cout << "RS | Best: " << rs.get_makespan()
              << " | Worst: " << worst_rs.get_makespan()
              << " | Average: " << avg_rs << " | Std: " << std_rs << "\n";
    std::cout << "Gd : " << gr.get_makespan() << "\n";
    std::cout << "SA | Best: " << sa.get_makespan()
              << " | Worst: " << worst_sa.get_makespan()
              << " | Average : " << avg_sa << " | Std: " << std_sa << "\n";
    std::cout << "GA | Best: " << ga.get_makespan()
              << " | Worst: " << worst_ga.get_makespan()
              << " | Average: " << avg_ga << " | Std: " << std_ga << "\n";

    std::cout << "Jobs: " << inst.n_jobs << "\n";
    std::cout << "Machines: " << inst.n_machines << "\n";
    std::cout << "UB: " << inst.UB << "\n";
    std::cout << "LB: " << inst.LB << "\n";
    return 0;
}