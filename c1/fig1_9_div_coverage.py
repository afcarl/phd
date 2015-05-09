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


N = 500
TAU = 0.05

graphs.output_file('c1_fig1_9_div_coverage.html')


for env_name in ['kin20_150']:
    for ex_name in ['random.motor', 'random.goal']:
        random.seed(0)

        # instanciating the environment
        env_cfg = envs.catalog[env_name]._deepcopy()
        env = environments.Environment.create(env_cfg)

        ex_cfg = exs.catalog[ex_name]._deepcopy()
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # running the exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

        # making graphs
        cov = factored.run_coverage(TAU, s_vectors)
        graphs.coverage(env.s_channels, TAU, s_vectors=s_vectors, c_alpha=1.0,
                        title='cov={:.2f} {}::{}'.format(cov, ex_name, env_name))
        graphs.hold(True)
        graphs.spread(env.s_channels, s_vectors=s_vectors,
                      e_radius=2.0, e_alpha=1.0,
                      title='{}:{}'.format(env_name, ex_name))


graphs.show()
