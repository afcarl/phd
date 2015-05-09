# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random

import explorers
import environments

import dotdot
import factored
import graphs
import exs
import envs


DIM = 100
N = 10000

graphs.output_file('c3_fig3_17_constraints.html')


for ex_name in ['random.motor']:
    for limit in [1, 2.5, 5, 10, 20, 45, 90, 150, 180]:
        random.seed(0)

        # instanciating the environment
        env_name, env_cfg = envs.kin(dim=DIM, limit=limit)
        env = environments.Environment.create(env_cfg)

        # instanciating the explorer
        ex_cfg = exs.catalog[ex_name]._deepcopy()
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # running the exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

        # making graphs
        graphs.spread(ex.s_channels, s_vectors=s_vectors,
                      e_radius=1.0, e_alpha=0.35,
                      title='{} {}'.format(ex_name, env_name))
        graphs.hold(True)
        alpha = 0.5 if limit < 90 else 1.0
        graphs.posture_idxs(env, explorations, alpha=alpha, idxs=[0, 1000, 2500, 5000, 7500], radius_factor=0.35)


graphs.show()
