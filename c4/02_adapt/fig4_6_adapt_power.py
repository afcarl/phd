# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

from __future__ import division
import random

import numpy as np

import explorers
import environments

import dotdot
import exs
import envs
import factored
import graphs

from c3_graphlib import adapt_graphs
import fig4_4_adapt_ex

N = 5000
env_name = 'kin20_150'

tallies = []
graphs.output_file('c4_fig4_6_adapt_power.html')
for power in [1.0, 2.0, 4.0]:
    random.seed(0)

    # instanciating the environment, and the Meshgrid
    env_cfg = envs.catalog[env_name]._deepcopy()
    env = environments.Environment.create(env_cfg)

    ex_cfg = fig4_4_adapt_ex.ex_cfg._deepcopy()
    ex_cfg.diversity_power = power
    ex_cfg.ex_1.learner.m_disturb = 0.5
    ex_cfg.m_channels = env.m_channels
    ex_cfg.s_channels = env.s_channels
    ex = explorers.Explorer.create(ex_cfg)

    # running the exploration
    explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

    for i, weights in enumerate(ex.weight_history['data']):
        ex.weight_history['data'][i] = [1000*w for w in weights]
    tally_dict = adapt_graphs(ex.cfg, explorations, s_vectors, ex.weight_history, title='{}'.format(power))

    tallies.append((tally_dict['motor.babbling'], tally_dict['goal.babbling']))
    print('done {}: {}% motor babbling'.format(power, 100.0*tally_dict['motor.babbling']/(tally_dict['goal.babbling']+tally_dict['motor.babbling'])))

# from bokeh import plotting

# percents = [100.0*tally[0]/(sum(tally)) for tally in tallies]
# plotting.quad(top=percents, left =[i   for i, _ in enumerate(percents)],
#               bottom=0,     right=[i+0.3 for i, _ in enumerate(percents)],
#               y_range = (0.0, 100.0), plot_width=300, plot_height=300,
#               fill_alpha=0.5, line_color=None,
#               title='percentage of use of motor babbling')
# plotting.xaxis().minor_tick_line_color = None
# plotting.xaxis().major_tick_line_color = None
# plotting.yaxis().minor_tick_line_color = None
# plotting.yaxis().major_tick_in = 0
# plotting.grid().grid_line_color = 'white'

graphs.show()
