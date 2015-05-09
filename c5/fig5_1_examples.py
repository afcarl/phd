# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random
import copy

import environments

import dotdot
import envs
import graphs


DIM = 20
RANGE = 150


# instanciating the two environments
env_name, env_cfg = envs.kin(dim=DIM, limit=RANGE)
env = environments.Environment.create(env_cfg)

lengths = [0.9**i for i in range(DIM)]
lengths = [s/sum(lengths) for s in lengths]
env2_name, env2_cfg = envs.kin(dim=DIM, limit=RANGE, lengths=lengths)
env2 = environments.Environment.create(env2_cfg)


# defining postures
random.seed(0)
m_channels = copy.deepcopy(env.m_channels)
for i in range(DIM-1):
    m_channels[i].bounds = (-45, 45)
m_signals = [environments.tools.random_signal(m_channels) for _ in range(50)]


# selecting some proeminent postures
selected = [m_signals[i] for i in [0, 1, 2, 3, 5, 9]]


# spreading their first joints to avoid superpositions
m_signals[0]['j{}'.format(DIM-1)] =  100.0
m_signals[1]['j{}'.format(DIM-1)] = -150.0
m_signals[2]['j{}'.format(DIM-1)] =  -30.0
m_signals[3]['j{}'.format(DIM-1)] =   50.0
m_signals[5]['j{}'.format(DIM-1)] =  -50.0
m_signals[9]['j{}'.format(DIM-1)] =   20.0


# making graphs
graphs.output_file('c5_fig5_1_examples.html')
for kin_env, color in zip([env, env2], ['#666666', '#E84A5F']):
    graphs.posture_signals(kin_env, m_signals,
                           color=color, alpha=0.1, radius_factor=0.5)
    graphs.hold(True)
for kin_env, color in zip([env, env2], ['#666666', '#E84A5F']):
    graphs.posture_signals(kin_env, selected,
                           color=color, alpha=0.75, radius_factor=0.5)
    graphs.hold(True)
graphs.hold(False)

graphs.posture_signals(env , [{'j{}'.format(i): 0 for i in range(20)}],
                       color='#666666', alpha=0.75, radius_factor=0.7,
                       x_range=[-0.1, 0.1], y_range=[-0.1, 1.1], plot_width=200)
graphs.posture_signals(env2, [{'j{}'.format(i): 0 for i in range(20)}],
                       color='#E84A5F', alpha=0.75, radius_factor=0.7,
                       x_range=[-0.1, 0.1], y_range=[-0.1, 1.1], plot_width=200)

graphs.show()

#'#2577B2', '#E84A5F'
