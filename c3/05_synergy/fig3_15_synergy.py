# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random

import numpy as np

import explorers
import environments

import dotdot
import exs
import envs
import graphs
import factored


DIM = 20
RES = 20
N   = 10000

# making graphs
graphs.output_file('c3_fig3_15_synergy.html')
timescale = [20000]
mesh_colors = ['#e5e5e5']


for ex_name in ['random.motor', 'random.goal']:
    for synergy in [2, None]:
        random.seed(0)

        # instanciating the environment, and the Meshgrid
        env_name, env_cfg = envs.kin(dim=DIM, limit=150, syn=synergy)
        env = environments.Environment.create(env_cfg)

        ex_cfg = exs.catalog[ex_name]._deepcopy()
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        mesh = explorers.ExplorerMeshGrid({'res': RES}, env.s_channels, env.m_channels)

        # running the exploration
        prefix = '{} {}'.format(env_name, ex_name)
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, mesh=mesh, prefix=prefix)

        # making graphs
        graphs.spread(ex.s_channels, s_vectors=s_vectors,
                      e_radius=1.3, e_alpha=0.35,
                      title='{} {}'.format(env_name, ex_name))
        graphs.hold(True)
        graphs.posture_idxs(env, explorations, alpha=1.0, idxs=[0, 1000, 2500, 5000, 7500], radius_factor=0.75)
        # graphs.posture_extrema(env, explorations, alpha=1.0, radius_factor=0.75)

graphs.show()
