# Design Space Exploration

Find the optimal parameter values minimizing the number of experiments to accurately profile selected system behaviors.

Designing and conducting experiments mostly involve measuring certain observations while changing some parameters. The quality of the observations is determined by the number of measurements and the parameter values used during the measurements.

This tool allows minimize the number of measurements require by finding optimal set of parameters to run the experiments.

### Some example use-cases:

- Understanding how different parameters affect a certain measurements (e.g. arrival rate vs latency plots).
- Collecting data to train ML models.
- Designing experiments to conduct statistical comparisons (e.g. doubling more no. of cores doubles performance).

### Dependencies:

These are some mandatory dependencies. Use the same version as indicated below.

    pyro-ppl - v1.0.0
    torch    - v1.3.1


### Usage:

The basic usage is as follows

    # define the parameters and their bounds
    # explores only within the defined bounds
    parameters = {
            'concurrency': RandomInt(0, 100),
            'mem_ratio': RandomFloat(-1, 1),
    }

    # initiate an explorer
    explorer = Explorer(parameters, RESULT_OUTPUT_PATH)

    # run the exploration NO_OF_STEPS defined by the user
    results_df = explorer.explore(NO_OF_STEPS, EVAL_FUNC)

The EVAL_FUNC is the function that actually execute the experiment and return the measurements. It should follow the below template.

    def EVAL_FUNC(param_dict)

        # param_dict: dictionary with selected parameter values.
        #                  e.g. {
        #                          'concurrency': 54,
        #                          'mem_ratio': 0.323,
        #                        }

        # execute any step requires to conduct the exeriment
        # wait till the measurement is recieved

        return the mesurement


### Examples

examples.py includes an example of efficiently estimating the Styblinski-Tang function

Below is the result after exploring 45 data-points.

![plots Styblinski-Tang](figs/styblinski_tang.png)

- Bayesian + GP : data collected using explorer tool, interpolated using Gaussian Process regression.
- Bayesian + XGB : data collected using explorer tool, interpolated using XGBoost.
- Uniform random + GP : data collected by sampling randomly, interpolated using Gaussian Process regression.
- Uniform random + XGB : data collected by sampling randomly, interpolated using XGBoost.

Observed error compared to the true function:

    Bayesian + GP  | MSE : 0.09  | MAPE : 2.68
    Bayesian + XGB | MSE : 60.43 | MAPE : 59.31
    Uniform random + GP  | MSE : 21.46 | MAPE : 99.02
    Uniform random + XGB | MSE : 46.26 | MAPE : 81.82

* MSE : mean squared error
* MAPE : mean absolute percentage error
