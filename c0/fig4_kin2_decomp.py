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


N        = 50000
env_name = 'kin2_150'
ex_name  = 'random.motor'

random.seed(0)


# Instanciating the Environment, the Explorer
env_cfg = envs.catalog[env_name]._deepcopy()
env = environments.Environment.create(env_cfg)

ex_cfg = exs.catalog[ex_name]._deepcopy()
ex_cfg.m_channels = env.m_channels
ex_cfg.s_channels = env.s_channels
ex = explorers.Explorer.create(ex_cfg)

# Running the Exploration
explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)


# Splitting the trials
s_vectors_pos, s_vectors_neg = [], []
for explo, s_vector in zip(explorations, s_vectors):
    if explo[0]['m_signal']['j0'] > 0:
        s_vectors_pos.append(s_vector)
    else:
        s_vectors_neg.append(s_vector)


plotting.output_file('../../results/c0_fig4_kin2_decomp.html')

# Positive Graph
graphs.bokeh_spread(env.s_channels, s_vectors=s_vectors_pos,
                    e_radius=1.0, e_alpha=0.5,
                    title='{}::{} [positive]'.format(env_name, ex_name))
plotting.hold(True)
graphs.bokeh_kin(env, [{'j0': i, 'j1':-150+2*i} for i in range(150, -1, -10)],
                 color='#333333', alpha=0.5, swap_xy=True)
plotting.hold(False)

# Negative Graph
graphs.bokeh_spread(env.s_channels, s_vectors=s_vectors_neg,
                    e_radius=1.0, e_alpha=0.5,
                    title='{}::{} [negative]'.format(env_name, ex_name))
plotting.hold(True)
graphs.bokeh_kin(env, [{'j0': -i, 'j1':-150+2*i} for i in range(0, 151, 10)],
                 color='#333333', alpha=0.5, swap_xy=True)
plotting.hold(False)

plotting.show()
