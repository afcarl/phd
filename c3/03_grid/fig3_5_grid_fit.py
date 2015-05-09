# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random
import copy

import environments
import explorers

import dotdot
import factored
import graphs
import envs
import exs


N = 5000

graphs.output_file('c3_fig3_5_grid_fit.html')


for res, b, radius, tile_ratio in [(  3, 2.0, 1.3, 0.985),
                                   ( 20, 1.0, 1.3, 0.95 ),
                                   ( 40, 1.0, 1.3, 0.95 ),
                                   (100, 1.0, 1.0, 1.0  )]:
    random.seed(0)

    # instanciating the environment
    env_name, env_cfg = envs.kin(dim=20, limit=150)
    env               = environments.Environment.create(env_cfg)

    # instanciating the explorer
    ex_cfg            = exs.catalog['random.goal']._deepcopy()
    ex_cfg.eras       = (10, None)
    ex_cfg.m_channels = env.m_channels
    ex_cfg.s_channels = env.s_channels
    ex                = explorers.Explorer.create(ex_cfg)

    # instanciating the mesh
    mesh_s_channels           = copy.deepcopy(env.s_channels)
    mesh_s_channels[0].bounds = (-b, b)
    mesh_s_channels[1].bounds = (-b, b)
    mesh = explorers.ExplorerMeshGrid({'res': res}, mesh_s_channels, env.m_channels)

    # running the exploration
    explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, mesh=mesh)

    # making graphs
    graphs.mesh(mesh, s_vectors=s_vectors, tile_ratio=tile_ratio,
                mesh_colors=[graphs.C_COLOR_H], mesh_timescale=[10000],
                e_radius=radius, title='{}'.format(res))

graphs.show()
