# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

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


DIM = 20
N   = 5000


# preparing graphs
graphs.output_file('c4_fig4_4_adapt.html')

for disturb in [0.001, 0.05, 0.5]:
    random.seed(0)

    # instanciating the environment
    env_name, env_cfg = envs.kin(dim=DIM, limit=150)
    env = environments.Environment.create(env_cfg)

    # instanciating the explorer
    ex_cfg = fig4_4_adapt_ex.ex_cfg._deepcopy()
    ex_cfg.ex_1.learner.m_disturb = disturb
    ex_cfg.m_channels = env.m_channels
    ex_cfg.s_channels = env.s_channels
    ex = explorers.Explorer.create(ex_cfg)

    # running the exploration
    explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

    # making graphs
    for i, weights in enumerate(ex.weight_history['data']):
        ex.weight_history['data'][i] = [1000*w for w in weights]
    adapt_graphs(ex.cfg, explorations, s_vectors, ex.weight_history, title='{}'.format(disturb))

graphs.show()
