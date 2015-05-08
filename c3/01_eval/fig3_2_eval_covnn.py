# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random
import math

import explorers
import environments

import dotdot
import exs
import envs
import graphs
import factored


N = 10000
BUFF_SIZE = 0.05

from bokeh import plotting
plotting.output_file('../../../results/c3_fig3_2_eval_covnn.html')

colors = ['#2577B2', '#E84A5F']
y_ranges = [(0, 0.65), (0, math.pi)]

for kind, y_range in zip(['nn', 'cov'], y_ranges):
    for env_name in ['kin20_150']:
        for i, explorer_name in enumerate(['random.motor', 'random.goal']):
            random.seed(0)

            # Instanciating the Environment, the Explorer
            env_cfg = envs.catalog[env_name]._deepcopy()
            env = environments.Environment.create(env_cfg)

            ex_cfg = exs.catalog[explorer_name]._deepcopy()
            ex_cfg.m_channels = env.m_channels
            ex_cfg.s_channels = env.s_channels
            ex = explorers.Explorer.create(ex_cfg)

            # Running the Exploration
            explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

            # Graph
            stds = None
            ticks = [1, 2, 3, 4, 5, 10, 15, 20] + [j for j in range(25, N+1, 25)]
            if kind == 'cov':
                perf = factored.run_coverages(BUFF_SIZE, s_vectors, ticks=ticks)
                # perf = [factored.run_coverage(BUFF_SIZE, s_vectors[:j]) for j in range(1, N)]
            else:
                testset = factored.testset()
                perf, stds_ = factored.run_nns(testset, s_vectors, ticks=ticks)

            graphs.bokeh_stds(ticks, perf, stds, color=colors[i], title=kind, y_range=y_range,
                              plot_width=500, plot_height=300)
            plotting.hold(True)
            print('{} {}'.format(kind, explorer_name))
    plotting.hold(False)

plotting.show()
