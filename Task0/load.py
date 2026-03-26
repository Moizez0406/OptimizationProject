def load_taillard(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Clean lines S
    lines = [line.strip() for line in lines if line.strip()]

    # --- Find header line ---
    for idx, line in enumerate(lines):
        try:
            n_jobs, n_machines, seed, UB, LB = map(int, line.split())
            header_index = idx
            break
        except ValueError:
            continue

    # --- Find where numeric matrix starts ---
    data_start = None
    for idx in range(header_index + 1, len(lines)):
        try:
            list(map(int, lines[idx].split()))
            data_start = idx
            break
        except ValueError:
            continue

    # --- Read machine data ---
    machine_data = []
    for i in range(data_start, data_start + n_machines):
        row = list(map(int, lines[i].split()))
        machine_data.append(row)

    # --- Transpose to job-major ---
    jobs = []
    for j in range(n_jobs):
        job = [machine_data[m][j] for m in range(n_machines)]
        jobs.append(job)

    return n_jobs, n_machines, jobs, UB, LB
