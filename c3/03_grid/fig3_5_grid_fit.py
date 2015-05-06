import random
import copy

from bokeh import plotting

import environments
import explorers
from environments import tools
from explorers import ExplorerMeshGrid

import dotdot
import factored
import graphs
import envs
import exs


N = 5000

plotting.output_file('../../../results/c3_fig3_5_grid_fit.html')


for res, b, tile_ratio in [(3, 2.0, 0.99), (20, 1.0, 0.97),  (40, 1.0, 0.97), (100, 1.0, 1.0)]:
    random.seed(0)

    # Configs
    env_cfg     = envs.catalog['kin20_150']._deepcopy() # kin20_90
    ex_cfg      = exs.catalog['random.goal']._deepcopy()
    ex_cfg.eras = (10, None)

    # Instanciating the Environment, the Explorer, and the Meshgrid
    env = environments.Environment.create(env_cfg)
    ex_cfg.m_channels = env.m_channels
    ex_cfg.s_channels = env.s_channels
    ex = explorers.Explorer.create(ex_cfg)

    mesh_s_channels           = copy.deepcopy(env.s_channels)
    mesh_s_channels[0].bounds = (-b, b)
    mesh_s_channels[1].bounds = (-b, b)
    mesh = ExplorerMeshGrid({'res': res}, mesh_s_channels, env.m_channels)

    # Running the Exploration
    explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, mesh=mesh)

    # Graph
    graphs.bokeh_mesh(mesh, s_vectors=s_vectors, tile_ratio=tile_ratio,
                      mesh_colors=[graphs.C_COLOR_H], mesh_timescale=[10000],
                      e_radius=1.3,
                      title='{}'.format(res))

plotting.show()
