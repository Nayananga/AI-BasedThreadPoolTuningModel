from simulation_utilities import ploting

data = []


def workload_generator(length):
    k = 10
    for i in range(length):
        if i % 100 == 0:
            k += 50

        data.append(k)

    ploting.general_plot(data)
    return data


def workload_config(def_workload, number_iterations):
    if len(def_workload) > number_iterations:
        workload = def_workload[:number_iterations]
    elif len(def_workload) < number_iterations:
        workload = []
        while len(workload) < number_iterations:
            workload = workload + def_workload
        workload = workload[:number_iterations]
    else:
        workload = def_workload

    return workload
