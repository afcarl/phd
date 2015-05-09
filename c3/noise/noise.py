import random
import copy

import explorers
import environments

import dotdot
import envs
import exs
import factored
import graphs


N = 10000
P_NOISE = 0.01

# making graphs
graphs.output_file('c3_noise.html')

def add_noise(signal, channels, p):
    """Return a noisy signal"""
    noisy_signal = copy.deepcopy(signal)
    for c, v in noisy_signal.items():
        v_min, v_max = channels[0].bounds
        noisy_signal[c] = random.uniform(max(v_min, v - p*(v_max-v_min)),
                                         min(v_max, v + p*(v_max-v_min)))
    return noisy_signal

env_name = 'kin20_150'

sm_noises = [[0.0, 0.0], [0.0,  0.01], [0.0,  0.02], [0.0,  0.05], [0.0, 0.1], [0.0, 0.2], [0.0, 0.5], [0.0, 1.0],
                         [0.01,  0.0], [0.02,  0.0], [0.05,  0.0], [0.1, 0.0], [0.2, 0.0], [0.5, 0.0], [1.0, 0.0],
                         [0.01, 0.01], [0.02, 0.02], [0.05, 0.05], [0.1, 0.1], [0.2, 0.2], [0.5, 0.5], [1.0, 1.0]]

for s_noise, m_noise in sm_noises:
    random.seed(0)

    # instanciating the environment, and the Meshgrid
    env_cfg = envs.catalog[env_name]
    env = environments.Environment.create(env_cfg)

    ex_cfg = exs.catalog['random.goal']._deepcopy()
    ex_cfg.m_channels = env.m_channels
    ex_cfg.s_channels = env.s_channels
    ex = explorers.Explorer.create(ex_cfg)

    # running the exploration
    explorations, s_vectors, s_goals = [], [], []

    for i in range(N):
        exploration = ex.explore()
        # adding motor noise
        m_signal = add_noise(exploration['m_signal'], env.m_channels, m_noise)
        feedback = env.execute(m_signal)
        s_vectors.append(environments.tools.to_vector(feedback['s_signal'], env.s_channels))
        # adding sensory noise
        feedback['s_signal'] = add_noise(feedback['s_signal'], env.s_channels, s_noise)
        ex.receive(exploration, feedback)

    graphs.bokeh_spread(env.s_channels, s_vectors=s_vectors,
                        e_radius=1.25, e_alpha=0.25,
                        title='{}::s:{}:m:{}'.format(env_name, s_noise, m_noise))

graphs.show()
