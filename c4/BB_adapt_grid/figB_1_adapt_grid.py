from __future__ import division
import random

import numpy as np

import explorers
import environments

import dotdot
import exs
import envs
import factored
import graphs

from c3_graphlib import adapt_graphs
import fig4_4_adapt_ex


N = 5000

# making graphs
graphs.output_file('c4_figB_1_adapt_grid.html')

#for disturb in [0.001, 0.005, 0.025, 0.05, 0.1, 0.2, 0.5, 1.0]:
for disturb in [0.001, 0.05, 0.5]:
    for res in [20, 40]:
        random.seed(0)

        # instanciating the environment
        env_name, env_cfg = envs.kin(dim=20, limit=150)
        env = environments.Environment.create(env_cfg)

        # instanciating the explorer
        ex_cfg = fig4_4_adapt_ex.grid_cfg._deepcopy()
        ex_cfg.res = res
        ex_cfg.ex_1.learner.m_disturb = disturb
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # running the exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, verbose=False)

        # making graphs
        adapt_graphs(ex_cfg, explorations, s_vectors, ex.weight_history, mesh=ex._diversity._meshgrid,
                     title='{} :: {}'.format(disturb, res))
        print('done {}'.format(disturb))


graphs.show()
