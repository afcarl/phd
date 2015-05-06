from __future__ import division, print_function

import random

from bokeh import plotting

import environments
from environments import tools

import dotdot
import graphs

import envs

def display_signals(env, m_signals, title='title', color='#666666', **kwargs):
    s_signals = [env.execute(m_signal)['s_signal'] for m_signal in m_signals]
    s_vectors = [environments.tools.to_vector(s_signal, env.s_channels) for s_signal in s_signals]

    graphs.bokeh_kin(env, m_signals, color=color, swap_xy=True, title=title, **kwargs)
    plotting.hold(False)
#    graphs.bokeh_spread(env.s_channels, s_vectors=s_vectors, e_color='red', e_radius=0.01, e_alpha=1.0, radius_units='data', swap_xy=True)

def display_vectors(env, m_vectors, title='title', color='#666666', **kwargs):
    m_signals = [environments.tools.to_signal(m_vector, env.m_channels) for m_vector in m_vectors]
    return display_signals(env, m_signals, title=title, color=color, **kwargs)

if __name__ == '__main__':
    env_cfg = envs.catalog['kin2_150']._deepcopy()
    env = environments.Environment.create(env_cfg)

    plotting.output_file('../../results/c0_kin_examplars.html')

    m_vectors = []
    for i in range(-150, 151, 20):
        m_vectors.append((150, i))
        m_vectors.append((135, i))

    display_vectors(env, m_vectors)

    m_vectors = []
    for i in range(-145, 151, 20):
        m_vectors.append(( 0,  i))
        m_vectors.append((15,  i-5))

    display_vectors(env, m_vectors)

    m_vectors = []
    for i in range(-150, 151, 10):
        m_vectors.append((i,  150))
        m_vectors.append((i, -150))

    display_vectors(env, m_vectors)

    plotting.show()

def display_random_m_vectors(env, explorations, n=5, **kwargs):
    m_display = choice_m_vectors(env.m_channels, explorations, n=n)
    display_vectors(env, m_display, **kwargs)

def choice_m_vectors(m_channels, explorations, n=5):
    """FIXME: no replacements"""
    m_vectors = []
    for _ in range(n):
        explo = random.choice(explorations)
        m_vector = tools.to_vector(explo[0]['m_signal'], m_channels)
        m_vectors.append(m_vector)

    return m_vectors
