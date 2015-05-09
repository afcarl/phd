import random


import explorers
import environments

import dotdot
import exs
import envs
import graphs
import factored


N     = 10000 # number of steps
DIM   = 100   # number of joints
LIMIT = 150   # joint range = [-LIMIT, +LIMIT]

graphs.output_file('c3_fig3_19_demo_control_{}.html'.format(DIM))


for ex_name in ['random.goal']:
    random.seed(0)

    # instanciating the environment
    env_name, env_cfg = envs.kin(dim=DIM, limit=LIMIT)
    env = environments.Environment.create(env_cfg)

    # instanciating the explorer
    ex_cfg = exs.catalog[ex_name]._deepcopy()
    ex_cfg.m_channels = env.m_channels
    ex_cfg.s_channels = env.s_channels
    ex = explorers.Explorer.create(ex_cfg)

    # running exploration
    explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, verbose=True)

    # making graphs
    for t1, t2 in [(0, 100), (100, N)]:
        alpha = 1.0 if t2 == 100 else 0.25
        graphs.posture_random(env, explorations[t1:t2], n=10,
                              alpha=0.75, radius_factor=0.35)
        graphs.hold(True)
        graphs.bokeh_spread(env.s_channels, s_vectors=s_vectors[:t2],
                            e_radius=1.5, e_alpha=alpha,
                            x_range=(-1.05, 1.05), y_range=(-1.05, 1.05),
                            title='{}::{}'.format(ex_name, env_name))

graphs.show()
