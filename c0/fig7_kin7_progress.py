# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random

import explorers
import environments

import dotdot
import exs
import envs
import graphs
import factored


N = 10000
milestones = [100, 200, 500, 1000, 2000, 3000, 4000, 5000, 5500, 6000, 7000, 8000, 9000, 100000]

graphs.output_file('c0_fig7_kin7_progress.html')


def find_rightmost(s_vectors, x_min, x_max):
    max_y, max_idx = -1, -1
    for i, (x, y) in enumerate(s_vectors):
        if x_min < x < x_max:
            if y > max_y:
                max_y   = y
                max_idx = i
    return max_idx

for env_name in ['kin7_150']:
    for ex_name in ['random.goal']:
        random.seed(0)

        # instanciating the environment
        env_cfg = envs.catalog[env_name]._deepcopy()
        env = environments.Environment.create(env_cfg)

        # instanciating the explorer
        ex_cfg = exs.catalog[ex_name]._deepcopy()
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # running the exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

        # making graphs
        for t in milestones:
            idxs = []
            for x_ in range(10):
                idxs.append(find_rightmost(s_vectors[:t], -x_/10.0, -(x_-1)/10.0))
            idxs.append(find_rightmost(s_vectors[:t], -0.960, -0.940))
            idxs.append(find_rightmost(s_vectors[:t], -0.940, -0.920))
            idxs.append(find_rightmost(s_vectors[:t], -0.920, -0.900))
            idxs.append(find_rightmost(s_vectors[:t], -0.900, -0.850))


            graphs.spread(env.s_channels, s_vectors=s_vectors[:t],
                          e_radius=1.4, e_alpha=0.5,
                          title='{}::{}::{}'.format(ex_name, env_name, t))

            for idx in idxs:
                graphs.hold(True)
                graphs.posture_signals(env, [explorations[idx][0]['m_signal']],
                                 color='#666666', alpha=0.50, radius_factor=0.6)

graphs.show()
