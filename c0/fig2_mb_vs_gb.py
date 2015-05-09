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


N = 10000

graphs.output_file('c0_fig2_mb_vs_gb.html')


for env_name in ['kin2_150', 'kin7_150', 'kin20_150', 'kin100_150']:
    for ex_name in ['random.motor', 'random.goal']:
        random.seed(0)

        # instanciating the environment
        env_cfg = envs.catalog[env_name]._deepcopy()
        env = environments.Environment.create(env_cfg)

        # instanciating the explorer
        ex_cfg = exs.catalog[ex_name]._deepcopy()
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # running the exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

        # making graphs
        graphs.spread(env.s_channels, s_vectors=s_vectors,
                      e_radius=1.3, e_alpha=0.5,
                      title='{}::{}'.format(ex_name, env_name))


graphs.show()
