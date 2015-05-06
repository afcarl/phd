from __future__ import division

import random

import learners
import explorers
import environments

import dotdot
import bokeh_kin
import factored
import graphs
import exs
import envs


DIM = 100
N = 10000

from bokeh import plotting
plotting.output_file('../../../results/c3_fig3_19_demo_{}.html'.format(DIM))

learn1_cfg = learners.DisturbLearner.defcfg._deepcopy()
learn1_cfg.m_disturb = 0.05

learn2_cfg = learners.DisturbTwoStepLearner.defcfg._deepcopy()
learn2_cfg.m_disturb = 0.05

lwlr_cfg = learners.ModelLearner.defcfg._copy(deep=True)
lwlr_cfg.models.fwd = 'ES-LWLR'
lwlr_cfg.models.inv = 'L-BFGS-B'

plwlr_cfg = learners.PredictDisturbLearner.defcfg._copy(deep=True)
plwlr_cfg.attempts    = 10
plwlr_cfg.m_disturb   = 0.05
plwlr_cfg.fwd         = lwlr_cfg


#for r in [5, 10, 20, 45, 90, 150, 180]:
for r in [150]:
    for learn_cfg in [learn1_cfg]:#, learn2_cfg]: #, plwlr_cfg]:
        random.seed(0)

        # Instanciating the Environment, the Explorer, and the Meshgrid
        env_cfg = envs.catalog['kin{}_{}'.format(DIM, r)]._deepcopy()
        env = environments.Environment.create(env_cfg)

        # Reuse Explorer Config
        ex_cfg                = explorers.MetaExplorer.defcfg._deepcopy()
        ex_cfg.eras           = (1, None)
        ex_cfg.weights        = ((1.0, 0.0), (0.0, 1.0))
        ex_cfg.fallback       = 0

        ex_cfg.ex_0           = explorers.ManualReuseExplorer.defcfg._deepcopy()
        ex_cfg.ex_1           = explorers.RandomGoalExplorer.defcfg._deepcopy()
        ex_cfg.ex_1.learner   = learn_cfg
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels

        dataset = {'m_channels': env.m_channels,
                   'm_signals': [{c.name: 0.0 for c in ex_cfg.m_channels}]}
        ex = explorers.Explorer.create(ex_cfg, datasets=[dataset])


        # Running the Exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, verbose=True)

        # Graphs
        milestones = [0, 100, 200, 500, 1000, 2000, 5000, N]
        for t in milestones[1:]:
            alpha = 0.5 if t == 100 else 0.25


            graphs.bokeh_spread(ex.s_channels, s_vectors=s_vectors[:t], s_goals=(),
                                e_radius=2.0, e_alpha=alpha,
                                x_range=(-1.05, 1.05), y_range=(-1.05, 1.05),
                                title='demo:t={}'.format(t))
            plotting.hold(True)
            bokeh_kin.display_signals(env, dataset['m_signals'], radius_factor=0.35, alpha=0.75)
            plotting.hold(True)
            graphs.bokeh_spread(ex.s_channels, s_vectors=s_vectors[:1], s_goals=(),
                                e_radius=2.0, e_alpha=.0, e_color='#DF6464')
            plotting.hold(True)
            bokeh_kin.display_random_m_vectors(env, explorations[milestones[milestones.index(t)-1]:], n=10,
                color='#666666', alpha=0.75, radius_factor=0.35)



plotting.show()
