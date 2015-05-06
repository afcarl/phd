import random

import forest
import explorers
import environments

import dotdot
import exs
import envs
import factored
import graphs


ARM_DIM = 20
RES     = 40
N       = 10000

# Graph
from bokeh import plotting
plotting.output_file('../../../results/c3_fig3_9_grid_unreach_{}.html'.format(RES))
timescale = [10, 100, 250, 500, 2000, 10000]
mesh_colors = graphs.colorscale(timescale, graphs.hex2rgb(graphs.C_COLOR), 0.16)


for a in [1.0, 2.0, 10.0]:
    for j in range(0, 101, 25):
        random.seed(0)

        # Instanciating the Environment, the Explorer, and the Meshgrid
        env_cfg = envs.catalog['kin{}_{}'.format(ARM_DIM, 150)]._deepcopy()
        env = environments.Environment.create(env_cfg)

        ex_cfg = exs.catalog['unreach_{}'.format(j)]._deepcopy()
        ex_cfg.ex_1.res   = int(a*RES)
        ex_cfg.ex_2.res   = int(a*RES)

        ex_bound = explorers.RestrictGoalExplorer.defcfg._deepcopy()
        ex_bound.manual_s_bounds = {'x': (-a, a), 'y': (-a, a)}
        ex_bound.explorer = ex_cfg._deepcopy()
        ex_bound.m_channels = env.m_channels
        ex_bound.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_bound)

        mesh_cfg = forest.Tree({'res': RES})
        mesh = explorers.ExplorerMeshGrid(mesh_cfg, env.s_channels, env.m_channels)

        # Running the Exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, mesh=mesh)

        # graphs
        graphs.bokeh_mesh(mesh, s_vectors=s_vectors, s_goals=s_goals,
                          mesh_colors=mesh_colors, mesh_timescale=timescale,
                          e_radius=1.0, e_alpha=0.55,
                          g_radius=1.0, g_alpha=0.35,
                          title='{} - {}%'.format(a, j))

        print('{}% done'.format(j))

plotting.show()
