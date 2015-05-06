import random

from bokeh import plotting

import forest
import learners
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

# preparing graphs
plotting.output_file('../../../results/c3_fig3_11_frontier_{}.html'.format(RES))
timescale = [10, 100, 250, 500, 2000, 10000]
mesh_colors = graphs.colorscale(timescale, graphs.hex2rgb(graphs.C_COLOR), 0.16)

# common explorer configuration
learn_cfg = learners.DisturbLearner.defcfg._deepcopy()
learn_cfg.m_disturb = 0.05

RES = 40
_ex_cfg              = explorers.MetaExplorer.defcfg._deepcopy()
_ex_cfg.eras         = (10, None)

_ex_cfg.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()

_ex_cfg.ex_1         = explorers.MeshgridGoalExplorer.defcfg._deepcopy()
_ex_cfg.ex_1.learner = learn_cfg
_ex_cfg.ex_1.res     = 2*RES

_ex_cfg.ex_2         = explorers.FrontierGoalExplorer.defcfg._deepcopy()
_ex_cfg.ex_2.learner = learn_cfg
_ex_cfg.ex_2.res     = 2*RES


for p in range(0, 101, 25):
    random.seed(0)

    # instanciating the environment
    env_cfg = envs.catalog['kin{}_{}'.format(ARM_DIM, 150)]._deepcopy()
    env = environments.Environment.create(env_cfg)

    # instantiating the explorer
    ex_cfg         = _ex_cfg._deepcopy()
    ex_cfg.weights = ((1.0, 0.0, 0.0), (0.0, 1.0-p/100.0, p/100.0))

    ex_bound = explorers.RestrictGoalExplorer.defcfg._deepcopy()
    ex_bound.manual_s_bounds = {'x': (-2, 2), 'y': (-2, 2)}
    ex_bound.explorer = ex_cfg._deepcopy()
    ex_bound.m_channels = env.m_channels
    ex_bound.s_channels = env.s_channels
    ex = explorers.Explorer.create(ex_bound)

    mesh_cfg = forest.Tree({'res': RES})
    mesh = explorers.ExplorerMeshGrid(mesh_cfg, env.s_channels, env.m_channels)

    # running the exploration
    explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, mesh=mesh)

    # making graphs
    graphs.bokeh_mesh(mesh, s_vectors=s_vectors, s_goals=s_goals,
                      mesh_colors=mesh_colors, mesh_timescale=timescale,
                      e_radius=1.0, e_alpha=0.55,
                      g_radius=1.0, g_alpha=0.25,
                      title='frontier - {}%'.format(p))

    print('frontier {}% done'.format(p))

plotting.show()
