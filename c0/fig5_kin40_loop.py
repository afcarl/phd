import random

from bokeh import plotting

import explorers
import environments

import dotdot
import exs
import envs
import graphs
import factored



N     = 10000 # number of steps
DIM   = 40    # number of joints
LIMIT = 150   # joint range = [-LIMIT, +LIMIT]

plotting.output_file('../../results/c0_fig5_kin40_loop.html')


for ex_name in ['random.goal']:
    random.seed(0)

    # instanciating the environment
    env_cfg = envs.kin(dim=DIM, limit=LIMIT)
    env = environments.Environment.create(env_cfg)

    # instanciating the explorer
    ex_cfg = exs.catalog[ex_name]._deepcopy()
    ex_cfg.m_channels = env.m_channels
    ex_cfg.s_channels = env.s_channels
    ex = explorers.Explorer.create(ex_cfg)

    # running exploration
    explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, verbose=True)

    # finding leftmost posture
    min_y, min_idx = 0, -1
    for i, (x, y) in enumerate(s_vectors):
        if y < min_y:
            min_y   = y
            min_idx = i

    # making graphs
    graphs.bokeh_spread(env.s_channels, s_vectors=s_vectors,
                        e_radius=1.5, e_alpha=0.25, plot_height=250, plot_width=800,
                        y_range=[-1, 0.05], x_range=[-1.05/8, 1.05/8],
                        title='{}::{}'.format(ex_name, 'kin{}_{}'.format(DIM, LIMIT)))
    plotting.hold(True)
    graphs.bokeh_kin(env, [explorations[min_idx][0]['m_signal']],
                     color='#666666', alpha=0.75, radius_factor=0.35)

plotting.show()
