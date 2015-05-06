import random

from bokeh import plotting

import explorers
import learners
import environments

import dotdot
import exs
import envs
import factored
import graphs


ARM_DIM = 20
RES     = 20
N       = 10000

plotting.output_file('../../../results/c3_fig3_13_inverse.html')


for disturb in [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.5, 1.0]:
    for env_name in ['kin2_150', 'kin7_150', 'kin20_150']:
        random.seed(0)

        print(disturb, env_name)
        # instanciating the environment
        env_cfg = envs.catalog[env_name]
        env = environments.Environment.create(env_cfg)

        # instanciating the explorer
        ex_cfg = exs.catalog['random.goal']._deepcopy()
        ex_cfg.ex_1.learner.m_disturb = disturb
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # running the exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, verbose=True)

        # making graphs
        radius = {0.001: 1.0, 0.005: 1.0}.get(disturb, 1.25)
        graphs.bokeh_spread(env.s_channels, s_vectors=s_vectors, s_goals=s_goals,
                            e_radius=radius, e_alpha=0.25, g_color=None,
                            title='{}::{}'.format(env_name, disturb))

plotting.show()
