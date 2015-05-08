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
import graphs
import factored


N = 50000
env_name      = 'kin2_150'
explorer_name = 'random.goal'

plotting.output_file('../../results/c0_fig6_kin2_gb.html'.format(int(N/1000)))


random.seed(0)

# instanciating the environment
env_cfg = envs.catalog[env_name]._deepcopy()
env = environments.Environment.create(env_cfg)

# instanciating the explorer
ex_cfg = exs.catalog[explorer_name]._deepcopy()
ex_cfg.m_channels = env.m_channels
ex_cfg.s_channels = env.s_channels

ex = explorers.Explorer.create(ex_cfg)

# running the Exploration
explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

# making graphs
graphs.bokeh_spread(env.s_channels, s_vectors=s_vectors,
                    e_radius=1.0, e_alpha=0.25,
                    title='{}::{}'.format(explorer_name, env_name))
plotting.hold(True)

m_vectors = [(150, 103), (135, 110), (  0, -45), ( 15, -50)]
m_signals = [environments.tools.to_signal(m_vector, env.m_channels) for m_vector in m_vectors]
graphs.bokeh_kin(env, m_signals, color='#333333', alpha=1.0)

plotting.show()
