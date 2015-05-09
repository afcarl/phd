from __future__ import division
import random

import numpy as np

import explorers
import learners
import environments

import dotdot
import envs
import factored
import graphs

from c3_graphlib import adapt_graphs
import fig4_8_adapt_reach_ex


N = 5000

graphs.output_file('c4_figB_3_adaptg_reach.html')

for RES in [20, 40]:
    random.seed(0)

    # instanciating the environment
    env_name = 'kin20_150'
    env_cfg  = envs.catalog[env_name]._deepcopy()
    env      = environments.Environment.create(env_cfg)

    # instanciating the explorer
    ex_cfg = fig4_8_adapt_reach_ex.grid_cfg._deepcopy()
    ex_cfg.ex_1.div_algorithm = 'grid'
    ex_cfg.ex_1.res = RES
    ex_cfg.ex_1.ex_0.res  = RES
    ex_cfg.ex_1.ex_1.res  = RES
    ex_cfg.m_channels     = env.m_channels
    ex_cfg.s_channels     = env.s_channels
    ex = explorers.Explorer.create(ex_cfg)

    # running the exploration
    explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

    # making graphs
    weight_history = ex.explorers[1].weight_history
    for i, weights in enumerate(weight_history['data']):
        weight_history['data'][i] = [1000*w for w in weights]
    adapt_graphs(ex_cfg.ex_1, explorations, s_vectors, weight_history, mesh=ex.explorers[1]._diversity._meshgrid, title='{}'.format(RES))

graphs.show()
