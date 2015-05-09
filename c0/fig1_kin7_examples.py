# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import environments

import dotdot
import envs
import graphs


# instanciating the environment
env_cfg = envs.catalog['kin7_150']._deepcopy()
env = environments.Environment.create(env_cfg)

# defining postures
m_vectors = [(132.654, -108.829, -100.829,  12.724, 133.011, -76.348, -118.995),
             (-19.163,   69.503,   44.059, -88.545, -36.027,  76.281,    8.720),
             (138.239,   39.661,  -84.211,  15.735, -33.844, 104.375,   26.110),
             ( 19.678,  -95.130,   96.038,  -7.118,  56.496,  10.632,  111.627),
             (135.685,   70.589,  -69.667,  -7.244, 149.627, -42.752,  -54.894),
            ]
m_signals = [environments.tools.to_signal(m_vector, env.m_channels) for m_vector in m_vectors]

# making graphs
graphs.output_file('c0_fig1_kin7_example.html')
graphs.posture_signals(env, m_signals, color='#666666', alpha=0.5)
graphs.show()
