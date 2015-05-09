# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random

import explorers
import environments

import dotdot
import exs
import envs
import factored
import graphs

from fig5_2_kin_reuse_picks import dataset, full_dataset, DIM, RES, N, MB
from fig5_2_kin_reuse_picks import env as env0


ARM_ALPHA  = 0.50
ARM_RADIUS = 0.75

env_cfg = environments.envs.KinematicArm2D.defcfg._deepcopy()
env_cfg.dim = DIM
#random.seed(290356442105405989)
#env_cfg.lengths = [random.random() for i in range(env_cfg.dim)]
env_cfg.lengths = [0.9**i for i in range(env_cfg.dim)]
env_cfg.lengths = [s/sum(env_cfg.lengths) for s in env_cfg.lengths]

env = environments.Environment.create(env_cfg)


random.seed(0)

# Reuse Explorer Config
ex_cfg                = explorers.MetaExplorer.defcfg._deepcopy()
ex_cfg.eras           = (MB, None)
ex_cfg.weights        = ((1.0, 0.0), (0.0, 1.0))
ex_cfg.fallback       = 0

ex_cfg.ex_0           = explorers.ReuseExplorer.defcfg._deepcopy()
ex_cfg.ex_0.reuse.res = RES
ex_cfg.ex_1           = explorers.RandomGoalExplorer.defcfg._deepcopy()
ex_cfg.ex_1.learner   = exs.catalog['random.goal'].ex_1.learner._deepcopy()

# instanciating the environment and the Explorer
ex_cfg.m_channels = env.m_channels
ex_cfg.s_channels = env.s_channels
ex = explorers.Explorer.create(ex_cfg, datasets=[dataset])

explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)


graphs.output_file('c5_fig5_2.3.4_reuse.html')

# Graph of reused effects in first env
s_vectors0 = []
for explo in explorations[:MB]:
    feedback = env0.execute(explo[0]['m_signal'])
    s_vectors0.append(explorers.tools.to_vector(feedback['s_signal'], env0.s_channels))

graphs.spread(env.s_channels, s_vectors=s_vectors0[:MB],
                    e_radius=3.0, e_alpha=1.0, e_color='#DF6464', title='first arm - reused effects')
for e in explorations[:MB]:
    graphs.hold(True)
    graphs.posture_signals(env0, [e[0]['m_signal']],
                           alpha=ARM_ALPHA, radius_factor=0.75)
graphs.hold(True)
graphs.spread(env.s_channels, s_vectors=s_vectors0[:MB], grid=False,
              e_radius=3.0, e_alpha=1.0, e_color='#DF6464')
graphs.hold(False)

# Graph Reuse
for t in [MB, 200, 400, N]:

    # alpha  = 1.0 if t != N else 0.5
    graphs.bokeh_spread(env.s_channels, s_vectors=s_vectors[MB:t],
                        e_radius=1.5, e_alpha=1.0, grid=False,
                        title='reuse :: {} steps'.format(t))
    if t == MB:
        for i in range(MB):
            graphs.hold(True)
            graphs.posture_signals(env, [explorations[i][0]['m_signal']],
                                   alpha=ARM_ALPHA, radius_factor=0.75)
    graphs.hold(True)
    graphs.spread(env.s_channels, s_vectors=s_vectors[:MB],
                  e_radius=3.0, e_alpha=1.0, e_color='#DF6464')
    graphs.hold(False)


    ## NoReuse ##

random.seed(0)

# NoReuse Explorer Config
ex2_cfg                = explorers.MetaExplorer.defcfg._deepcopy()
ex2_cfg.eras           = (MB, None)
ex2_cfg.weights        = ((1.0, 0.0), (0.0, 1.0))
ex2_cfg.fallback       = 0

ex2_cfg.ex_0           = explorers.RandomMotorExplorer.defcfg._deepcopy()
ex2_cfg.ex_0.learner   = exs.catalog['random.goal'].ex_1.learner._deepcopy()
ex2_cfg.ex_1           = explorers.RandomGoalExplorer.defcfg._deepcopy()
ex2_cfg.ex_1.learner   = exs.catalog['random.goal'].ex_1.learner._deepcopy()

# instanciating the environment and the Explorer
ex2_cfg.m_channels = env.m_channels
ex2_cfg.s_channels = env.s_channels
ex2 = explorers.Explorer.create(ex2_cfg)

explorations2, s_vectors2, s_goals2 = factored.run_exploration(env, ex2, N)

# making graphs
for t in [MB, 200, 400, N]:

    # alpha  = 1.0 if t != N else 0.5
    graphs.spread(env.s_channels, s_vectors=s_vectors2[MB:t],
                  e_radius=1.5, e_alpha=1.0, grid=False,
                  title='noreuse :: {} steps'.format(t))
    if t == MB:
        for i in range(MB):
            graphs.hold(True)
            graphs.posture_signals(env, [explorations2[i][0]['m_signal']],
                                   alpha=ARM_ALPHA, radius_factor=0.75)
    graphs.hold(True)
    graphs.spread(env.s_channels, s_vectors=s_vectors2[:MB], grid=False,
                  e_radius=3.0, e_alpha=1.0, e_color='#DF6464')
    graphs.hold(False)



    ## RandomReuse ##

random.seed(0)

# Random Reuse Explorer Config
ex3_cfg                = explorers.MetaExplorer.defcfg._deepcopy()
ex3_cfg.eras           = (MB, None)
ex3_cfg.weights        = ((1.0, 0.0), (0.0, 1.0))
ex3_cfg.fallback       = 0

ex3_cfg.ex_0           = explorers.ReuseExplorer.defcfg._deepcopy()
ex3_cfg.ex_0.reuse.algorithm = 'random'
ex3_cfg.ex_0.reuse.res = RES
ex3_cfg.ex_1           = explorers.RandomGoalExplorer.defcfg._deepcopy()
ex3_cfg.ex_1.learner   = exs.catalog['random.goal'].ex_1.learner._deepcopy()

# instanciating the environment and the Explorer
ex3_cfg.m_channels = env.m_channels
ex3_cfg.s_channels = env.s_channels
ex3 = explorers.Explorer.create(ex3_cfg, datasets=[full_dataset])

explorations3, s_vectors3, s_goals3 = factored.run_exploration(env, ex3, N)

# making graphs
for t in [MB, 200, 400, N]:

    # alpha  = 1.0 if t != N else 0.5
    graphs.spread(env.s_channels, s_vectors=s_vectors3[MB:t],
                  e_radius=1.5, e_alpha=1.0, grid=False,
                  title='randomreuse :: {} steps'.format(t))
    graphs.hold(True)
    graphs.spread(env.s_channels, s_vectors=s_vectors3[:MB],
                  e_radius=3.0, e_alpha=1.0, e_color='#DF6464')
    graphs.hold(False)

    if t == MB:
        for i in range(MB):
            graphs.hold(True)
            graphs.posture_signals(env, [explorations3[i][0]['m_signal']],
                                   alpha=0.50, radius_factor=0.75)
    graphs.hold(False)

graphs.show()



