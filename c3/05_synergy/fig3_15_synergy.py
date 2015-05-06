import random

import numpy as np

import forest
import explorers
import learners
import environments

import dotdot
import exs
import envs
import graphs
import factored


ARM_DIM = 20
RES     = 20
N       = 10000

# Graph
from bokeh import plotting
plotting.output_file('../../../results/c3_fig3_15_synergy.html')
#timescale = [10, 100, 250, 500, 5000, 20000]
#mesh_colors = graphs.colorscale(timescale, (233,  78, 119), 0.16)
timescale = [20000]
mesh_colors = ['#e5e5e5']


for explorer_name in ['random.motor', 'random.goal']: #to investigate (lower perf, higher std)
    for env_name in ['kinsyn20_2', 'kin20_150']:
        random.seed(0)

        # Instanciating the Environment, the Explorer, and the Meshgrid
        env_cfg = envs.catalog[env_name]
        env = environments.Environment.create(env_cfg)

        ex_cfg = exs.catalog[explorer_name]._deepcopy()
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # mesh_cfg = forest.Tree()
        mesh = explorers.ExplorerMeshGrid({'res': RES}, env.s_channels, env.m_channels)

        # Running the Exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, mesh=mesh, verbose=True)

        # Graphs
        graphs.bokeh_spread(ex.s_channels, s_vectors=s_vectors,
                            e_radius=1.3, e_alpha=0.5,
                            title='{} {}'.format(env_name, explorer_name))
        # graphs.bokeh_mesh(mesh, s_vectors=s_vectors, s_goals=s_goals,
        #                   mesh_colors=mesh_colors, mesh_timescale=timescale,
        #                   e_radius=1.3, e_alpha=0.5,
        #                   g_radius=1.0, g_alpha=0.5,
        #

        # errors = factored.run_nn(factored.testset(), s_vectors)
        # graphs.bokeh_nn(env.s_channels, factored.testset(), errors,
        #                 title='{} {} {:.3f}'.format(env_name, explorer_name, np.average(errors)),)

plotting.show()
