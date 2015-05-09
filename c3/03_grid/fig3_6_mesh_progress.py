# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random
import copy

import numpy as np

import explorers
import environments

import dotdot
import exs
import envs
import graphs


DIM = 20
RES = 20
N   = 10000

random.seed(0)


# instanciating the environment
env_name, env_cfg = envs.kin(dim=DIM, limit=150)
env               = environments.Environment.create(env_cfg)

# instanciating the explorer
ex_cfg            = exs.catalog['random.goal']._deepcopy()
ex_cfg.m_channels = env.m_channels
ex_cfg.s_channels = env.s_channels
ex                = explorers.Explorer.create(ex_cfg)

# instanciating the grid
mesh_s_channels = copy.deepcopy(env.s_channels)
mesh = explorers.ExplorerMeshGrid({'res': RES}, env.s_channels, env.m_channels)

# preparing graphs
graphs.output_file('c3_fig3_6_mesh_progression.html')
timescale = [10, 100, 250, 500, 2000, 10000]
colors = graphs.colorscale(timescale, graphs.hex2rgb(graphs.C_COLOR), 0.16)


# running the exploration
explorations, s_vectors = [], []
for t in range(N):
    exploration = ex.explore()
    feedback = env.execute(exploration['m_signal'])
    ex.receive(exploration, feedback)
    s_vectors.append(environments.tools.to_vector(feedback['s_signal'], env.s_channels))
    explorations.append((exploration, feedback))
    mesh.add(feedback['s_signal'])

    # making graphs
    if t+1 in timescale:
        e_radius, e_alpha = 1.5, 0.75
        if t+1 == N:
            e_alpha = 0.25
        graphs.mesh(mesh, s_vectors=s_vectors,
                    mesh_colors=colors, mesh_timescale=timescale,
                    e_radius=e_radius, e_alpha=e_alpha)


graphs.show()
