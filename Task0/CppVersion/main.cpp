<<<<<<< HEAD
#include <iostream>
=======
#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>
>>>>>>> 83805ac (Small fixes across all the project)

#include "Subject_solution.h"
#include "algo.h"
#include "load.h"

int main() {
<<<<<<< HEAD
=======
    std::ofstream outFile("results.csv");
    outFile << "Algorithm,Makespan\n";
>>>>>>> 83805ac (Small fixes across all the project)
    TaillardInstance inst = load_taillard("../tai100_10_0.fsp");
    Subject_solution::set_lookup(inst.jobs);
    Subject_solution sol(inst.jobs);

    const int RUNS = 20;
<<<<<<< HEAD

    int sum_rs = 0, sum_sa = 0, sum_ga = 0;
    int sumsq_rs = 0, sumsq_sa = 0, sumsq_ga = 0;

    Subject_solution rs = randomSearch(sol);
    Subject_solution sa = simulatedAnnealing(sol);
    Subject_solution ga = genetic(sol);
    Subject_solution gr = greedy(sol);

    Subject_solution worst_rs = rs;
    Subject_solution worst_sa = sa;
    Subject_solution worst_ga = ga;
=======
    int population_size = 180;
    int generations = 100;
    int tournament_size = 5;
    double pm = 0.1;

    // initialize with first run
    Subject_solution rs = randomSearch(sol);
    Subject_solution sa = simulatedAnnealing(sol);
    Subject_solution ga =
        genetic(sol, population_size, generations, tournament_size, pm);
    Subject_solution gr = greedy(sol);
    Subject_solution worst_rs = rs;
    Subject_solution worst_sa = sa;
    Subject_solution worst_ga = ga;
    Subject_solution worst_gr = gr;

    int sum_rs = 0, sum_sa = 0, sum_ga = 0, sum_gr = 0;
    int sumsq_rs = 0, sumsq_sa = 0, sumsq_ga = 0, sumsq_gr = 0;
>>>>>>> 83805ac (Small fixes across all the project)

    for (int i = 0; i < RUNS; i++) {
        Subject_solution curr_rs = randomSearch(sol);
        Subject_solution curr_sa = simulatedAnnealing(sol);
<<<<<<< HEAD
        Subject_solution curr_ga = genetic(sol);
=======
        Subject_solution curr_ga =
            genetic(sol, population_size, generations, tournament_size, pm);
        Subject_solution curr_gr = greedy(sol);  // ← called each iteration now
>>>>>>> 83805ac (Small fixes across all the project)

        int m_rs = curr_rs.get_makespan();
        int m_sa = curr_sa.get_makespan();
        int m_ga = curr_ga.get_makespan();
<<<<<<< HEAD
=======
        int m_gr = curr_gr.get_makespan();  // ← fresh value each run

        outFile << "RS," << m_rs << "\n";
        outFile << "GR," << m_gr << "\n";
        outFile << "SA," << m_sa << "\n";
        outFile << "GA," << m_ga << "\n";
>>>>>>> 83805ac (Small fixes across all the project)

        // ---- accumulate ----
        sum_rs += m_rs;
        sum_sa += m_sa;
        sum_ga += m_ga;
<<<<<<< HEAD

        sumsq_rs += m_rs * m_rs;
        sumsq_sa += m_sa * m_sa;
        sumsq_ga += m_ga * m_ga;
=======
        sum_gr += m_gr;
        sumsq_rs += m_rs * m_rs;
        sumsq_sa += m_sa * m_sa;
        sumsq_ga += m_ga * m_ga;
        sumsq_gr += m_gr * m_gr;
>>>>>>> 83805ac (Small fixes across all the project)

        // ---- BEST ----
        if (m_rs < rs.get_makespan()) rs = curr_rs.copy();
        if (m_sa < sa.get_makespan()) sa = curr_sa.copy();
<<<<<<< HEAD
        if (m_ga < ga.get_makespan()) ga = curr_ga;
=======
        if (m_ga < ga.get_makespan()) ga = curr_ga.copy();
        if (m_gr < gr.get_makespan()) gr = curr_gr.copy();
>>>>>>> 83805ac (Small fixes across all the project)

        // ---- WORST ----
        if (m_rs > worst_rs.get_makespan()) worst_rs = curr_rs.copy();
        if (m_sa > worst_sa.get_makespan()) worst_sa = curr_sa.copy();
<<<<<<< HEAD
        if (m_ga > worst_ga.get_makespan()) worst_ga = curr_ga;
    }
    double avg_rs = (double)sum_rs / RUNS;
    double avg_sa = (double)sum_sa / RUNS;
    double avg_ga = (double)sum_ga / RUNS;
=======
        if (m_ga > worst_ga.get_makespan()) worst_ga = curr_ga.copy();
        if (m_gr > worst_gr.get_makespan()) worst_gr = curr_gr.copy();
    }
    outFile.close();

    double avg_rs = (double)sum_rs / RUNS;
    double avg_sa = (double)sum_sa / RUNS;
    double avg_ga = (double)sum_ga / RUNS;
    double avg_gr = (double)sum_gr / RUNS;
>>>>>>> 83805ac (Small fixes across all the project)

    double std_rs = sqrt((double)sumsq_rs / RUNS - avg_rs * avg_rs);
    double std_sa = sqrt((double)sumsq_sa / RUNS - avg_sa * avg_sa);
    double std_ga = sqrt((double)sumsq_ga / RUNS - avg_ga * avg_ga);
<<<<<<< HEAD
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
=======
    double std_gr = sqrt((double)sumsq_gr / RUNS - avg_gr * avg_gr);

    std::cout << "RS | Best: " << rs.get_makespan()
              << " | Worst: " << worst_rs.get_makespan() << " | Avg: " << avg_rs
              << " | Std: " << std_rs << "\n";
    std::cout << "GR | Best: " << gr.get_makespan()
              << " | Worst: " << worst_gr.get_makespan() << " | Avg: " << avg_gr
              << " | Std: " << std_gr << "\n";
    std::cout << "SA | Best: " << sa.get_makespan()
              << " | Worst: " << worst_sa.get_makespan() << " | Avg: " << avg_sa
              << " | Std: " << std_sa << "\n";
    std::cout << "GA | Best: " << ga.get_makespan()
              << " | Worst: " << worst_ga.get_makespan() << " | Avg: " << avg_ga
              << " | Std: " << std_ga << "\n";
>>>>>>> 83805ac (Small fixes across all the project)

    std::cout << "Jobs: " << inst.n_jobs << "\n";
    std::cout << "Machines: " << inst.n_machines << "\n";
    std::cout << "UB: " << inst.UB << "\n";
    std::cout << "LB: " << inst.LB << "\n";
<<<<<<< HEAD
=======

>>>>>>> 83805ac (Small fixes across all the project)
    return 0;
}