import random

import explorers
import environments
from environments import tools

import dotdot
import factored
import graphs
import exs
import envs


DIM = 100
N = 10000

from bokeh import plotting
plotting.output_file('../../../results/c3_fig3_17_constraints.html')

for explorer_name in ['random.motor']:
    for r in [1, 2.5, 5, 10, 20, 45, 90, 150, 180]:
        random.seed(0)

        # instanciating the environment
        env_cfg = envs.catalog['kin{}_{}'.format(DIM, r)]._deepcopy()
        env = environments.Environment.create(env_cfg)

        # instanciating the explorer
        ex_cfg = exs.catalog[explorer_name]._deepcopy()
        ex_cfg.m_channels = env.m_channels
        ex_cfg.s_channels = env.s_channels
        ex = explorers.Explorer.create(ex_cfg)

        # running the exploration
        explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N)

        # making graphs
        graphs.bokeh_spread(ex.s_channels, s_vectors=s_vectors, s_goals=(),
                            e_radius=1.0, e_alpha=0.35,
                            title='{} {}'.format(explorer_name, r))

plotting.show()
