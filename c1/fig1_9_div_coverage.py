import random

from bokeh import plotting

import explorers
import environments

import dotdot
import exs
import envs
import graphs
import factored


N = 500
BUFF_SIZE = 0.05

plotting.output_file('../../results/c1_fig1_9_div_coverage.html')


for env_name in ['kin20_150']:
    for explorer_name in ['random.motor', 'random.goal']:
        random.seed(0)

        # Instanciating the Environment, the Explorer
        env_cfg = envs.catalog[env_name]._deepcopy()
        env = environments.Environment.create(env_cfg)

        ex_cfg = exs.catalog[explorer_name]._deepcopy()
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # Running the Exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

        # Graph
        cov = factored.run_coverage(BUFF_SIZE, s_vectors)
        graphs.bokeh_coverage(env.s_channels, BUFF_SIZE, s_vectors=s_vectors, c_alpha=1.0,
                              title='cov={:.2f} {}::{}'.format(cov, explorer_name, env_name))
        plotting.hold(True)
        graphs.bokeh_spread(env.s_channels, s_vectors=s_vectors,
                            e_radius=2.0, e_alpha=1.0)


plotting.show()
