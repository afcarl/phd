import random
import bisect
import copy

from bokeh import plotting

import numpy as np

import forest
import explorers
import environments
from environments import tools
from explorers import ExplorerMeshGrid

import dotdot
import exs
import envs
import graphs


ARM_DIM = 20
RES = 20
N = 10000

random.seed(0)


# instanciating the environment
env_cfg = envs.catalog['kin{}_{}'.format(ARM_DIM, 150)]._deepcopy()
env = environments.Environment.create(env_cfg)

# instanciating the explorer
ex_cfg = exs.catalog['random.goal']._deepcopy()
ex_cfg.m_channels = env.m_channels
ex_cfg.s_channels = env.s_channels
ex = explorers.Explorer.create(ex_cfg)

# instanciating the grid
mesh_cfg = forest.Tree({'res': RES})
mesh_s_channels = copy.deepcopy(env.s_channels)
mesh = ExplorerMeshGrid(mesh_cfg, env.s_channels, env.m_channels)

# preparing graphs
plotting.output_file('../../../results/c3_fig3_6_mesh_progression.html')
timescale = [10, 100, 250, 500, 2000, 10000]
colors = graphs.colorscale(timescale, graphs.hex2rgb(graphs.C_COLOR), 0.16)


# running the exploration
explorations, s_vectors = [], []
for t in range(N):
    exploration = ex.explore()
    feedback = env.execute(exploration['m_signal'])
    ex.receive(exploration, feedback)
    s_vectors.append(tools.to_vector(feedback['s_signal'], env.s_channels))
    explorations.append((exploration, feedback))
    mesh.add(feedback['s_signal'])

    if t+1 in timescale:
        e_radius, e_alpha = 1.5, 0.75
        if t+1 == N:
            e_alpha = 0.25
        # if timescale.index(i+1) != len(timescale)-1:
        #     e_radius, e_alpha = 1.25-0.05*timescale.index(i+1), 0.75-0.1*timescale.index(i+1)
        graphs.bokeh_mesh(mesh, s_vectors=s_vectors,
                          mesh_colors=colors, mesh_timescale=timescale,
                          e_radius=e_radius, e_alpha=e_alpha)


plotting.show()
