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


DIM = 20
N   = 10000
TAU = 0.05  # for coverage evalution

graphs.output_file('c3_fig3_2_eval_covnn.html')


ex_names   = ['random.motor', 'random.goal']
colors     = [graphs.MOTOR_COLOR,  graphs.GOAL_COLOR]

# evaluating with testset-based and coverage-based measure.
eval_kinds = [     'nn',        'cov']
y_ranges   = [(0, 0.65), (0, math.pi)]
ticks = [1, 2, 3, 4, 5, 10, 15, 20] + [j for j in range(25, N+1, 25)]


for kind, y_range in zip(eval_kinds, y_ranges):

    for ex_name, color in zip(ex_names, colors):
        random.seed(0)

        # instanciating the environment
        env_name, env_cfg = envs.kin(dim=DIM, limit=150)
        env = environments.Environment.create(env_cfg)

        ex_cfg = exs.catalog[ex_name]._deepcopy()
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # running the exploration
        prefix = '{} {}'.format(kind, ex_name, kind)
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, prefix=prefix)

        # making graphs
        if kind == 'cov':
            perf = factored.run_coverages(TAU, s_vectors, ticks=ticks)
        else:
            perf, _ = factored.run_nns(factored.testset(), s_vectors, ticks=ticks)

        graphs.perf_std(ticks, perf, None, color=color, title=kind, y_range=y_range,
                        plot_width=500, plot_height=300)
        graphs.hold(True)

    graphs.hold(False)

graphs.show()
