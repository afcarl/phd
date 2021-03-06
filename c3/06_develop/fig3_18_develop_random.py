# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random
import copy

import explorers
import environments
from environments import tools

import dotdot
import factored
import graphs
import exs
import envs


DIM   = 40
assert DIM % 2 == 0

LIMIT = 150
N     = 10000
REP   = 1


def update_m_channels(env, ex, m_center, r):
    """"Update the motor channels of the """
    m_channels = copy.deepcopy(ex.m_channels)
    for m_i, c_x, c_e in zip(m_center, m_channels, env.m_channels):
        c_x.bounds = (max(c_e.bounds[0], m_i-r),
                      min(c_e.bounds[1], m_i+r))
    ex._m_channels = m_channels
    ex.explorers[0]._m_channels = m_channels
    ex.explorers[1]._learners[0].virtual_m_channels = m_channels

# m_centers
random.seed(0)
m_centers = [(0, 0)*int(DIM/2)]

milestones = [ 0, 500,   N]
ranges     = [80, 150, 150]

lrns = {'disturb': exs.learn_cfg._deepcopy(),
        #'plwlr'  : exs.plwlr_cfg._deepcopy()
       }

ex_name = 'random.goal'

if __name__ == '__main__':
    graphs.output_file('c3_fig3_18_develop_random_{}.html'.format(DIM))

    for rep, m_center in enumerate(m_centers):
        for lrn_name, lrn_cfg in lrns.items():
            for milestones, ranges in [([0, 500, N], [150, 150, 150]), ([0, 500, N], [80, 150, 150])]:
                random.seed(0)

                # instanciating the environment, and the Meshgrid
                env_name, env_cfg = envs.kin(dim=DIM, limit=LIMIT)
                env = environments.Environment.create(env_cfg)

                ex_cfg = exs.catalog[ex_name]._deepcopy()
                ex_cfg.ex_1.learner = lrn_cfg
                ex_cfg.m_channels = env.m_channels
                ex_cfg.s_channels = env.s_channels
                ex = explorers.Explorer.create(ex_cfg)

                update_m_channels(env, ex, m_center, ranges[0])

                # running the exploration
                explorations, s_vectors, s_goals = [], [], []

                for t in range(N):
                    exploration = ex.explore()
                    feedback = env.execute(exploration['m_signal'])
                    ex.receive(exploration, feedback)
                    s_vectors.append(tools.to_vector(feedback['s_signal'], env.s_channels))
                    if 's_goal' in exploration:
                        s_goals.append(tools.to_vector(exploration['s_goal'], env.s_channels))
                    explorations.append((exploration, feedback))

                    if t+1 in milestones:
                        idx = milestones.index(t+1)
                        last_milestone = milestones[idx-1]
                        alpha = 0.75 if t+1 != N else 0.20
                        radius = 1.5 if t+1 != N else 1.5


                        # making graphs
                        print('{: 6.0f}: {} ({})'.format(t+1, ex.m_channels[0].bounds, lrn_name))
                        graphs.spread(ex.s_channels, s_vectors=s_vectors[:last_milestone],
                                      e_alpha=0.50,
                                      title=']{}, {}] period : {} ({})'.format(
                                            last_milestone, t+1, ex.m_channels[0].bounds, lrn_name))
                        graphs.hold(True)
                        graphs.spread(ex.s_channels, s_vectors=s_vectors[last_milestone:],
                                      e_alpha=alpha, e_radius=radius)
                        # display postures
                        graphs.hold(True)
                        graphs.posture_random(env, explorations[last_milestone:], n=5,
                            radius_factor=0.50)
                        graphs.hold(False)

                        # update m_channels
                        update_m_channels(env, ex, m_center, ranges[idx])


                min_y, min_idx = 0, -1
                for i, (x, y) in enumerate(s_vectors):
                    if y < min_y:
                        min_y   = y
                        min_idx = i

                # making graphs
                graphs.spread(env.s_channels, s_vectors=s_vectors,
                              e_radius=1.5, e_alpha=0.25, plot_height=250, plot_width=800,
                              y_range=[-1, 0.05], x_range=[-0.2, 0.1],
                              title='{}::{}'.format(ex_name, env_name))
                graphs.hold(True)
                graphs.posture_signals(env, [explorations[min_idx][0]['m_signal']],
                                       alpha=0.75, radius_factor=0.35)

    graphs.show()
