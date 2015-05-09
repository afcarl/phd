# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random

import explorers
import environments

import dotdot
import exs
import envs
import graphs
import factored


DIM = 7
N   = 5000

# preparing graphs
graphs.output_file('c4_fig4_1_mbratio.html')


ex_name = 'random.goal'

for p in [0.001, 0.05]:
    for era_length in [1, 10, 1000]:
        random.seed(0)

        # instanciating the environment, and the Meshgrid
        env_name, env_cfg = envs.kin(dim=DIM, limit=150)
        env = environments.Environment.create(env_cfg)

        ex_cfg = exs.catalog[ex_name]._deepcopy()
        ex_cfg.eras       = (era_length, None)
        ex_cfg.weights    = ((1.0, 0.0), (0.0, 1.0))
        ex_cfg.ex_1.learner.m_disturb = p
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # running the exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

        # making graphs
        alpha = 0.35 if p == 0.001 else 0.75
        graphs.bokeh_spread(ex.s_channels, s_vectors=s_vectors,
                            e_radius=1.0, e_alpha=alpha,
                            title='{}: p={} era={}'.format(env_name, p, era_length))
        graphs.hold(True)
        # graphs.posture_extrema(env, explorations,
        #                     alpha=0.5, radius_factor=0.75)
        graphs.posture_idxs(env, explorations, idxs=[4000 + i*50 for i in range(10)],
                            alpha=0.5, radius_factor=0.75)

graphs.show()
