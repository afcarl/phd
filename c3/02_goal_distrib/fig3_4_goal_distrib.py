# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random

from bokeh import plotting

import explorers
import environments

import dotdot
import exs
import envs
import factored
import graphs


N = 10000

graphs.output_file('c3_fig3_4_goal_distrib.html')

for env_name in ['kin2_150', 'kin20_150']:
    for ex_name, xy_range in [('random.motor',   1.0),
                              ('random.goal',    1.1),
                              ('distrib_corner', 1.1),
                              ('distrib0.5',     1.1),
                              ('distrib2',       2.2),
                              ('distrib10',     11.0),
                             ]:
        random.seed(0)

        # instanciating the environment, and the Meshgrid
        env_cfg = envs.catalog[env_name]._deepcopy()
        env = environments.Environment.create(env_cfg)

        ex_cfg = exs.catalog[ex_name]._deepcopy()
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # running the exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

        # making graphs
        radius, alpha = 1.0, 0.35
        if ex_name == 'distrib_corner':
            radius, alpha = 0.75, 0.15

        plotting.circle([0.0], [0.0], radius=1.0,
                        x_range=(-xy_range, xy_range), y_range=(-xy_range, xy_range),
                        fill_color='#000000', fill_alpha=0.075, line_color=None,
                        title='goal distribution for {}'.format(ex_name))
        graphs.hold(True)
        graphs.spread(ex.s_channels, s_vectors=(), s_goals=s_goals,
                      g_radius=radius, g_alpha=alpha, grid=None,
                      title='{} goals'.format(ex_name))

        graphs.spread(ex.s_channels, s_vectors=s_vectors, s_goals=(),
                      e_radius=1.0, e_alpha=0.35, grid=None,
                      title=ex_name)

graphs.show()
