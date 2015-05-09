# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os
import math

import numpy as np

from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

from fig4_2_mbratio_cluster import expcfgs_levels, cfg, env_names, disturbs


exp_cfgs = expcfgs_levels[0]
steps = cfg.job.steps

def load_data(kind):
    cwd = os.getcwd()

    Ns = [1000, 2000, 5000, 10000]
    ps, avgs, stds = ({(env, d, N): [] for env in env_names for d in disturbs for N in Ns},
                      {(env, d, N): {} for env in env_names for d in disturbs for N in Ns},
                      {(env, d, N): {} for env in env_names for d in disturbs for N in Ns})
    ds = [0.001, 0.05, 0.5]
    env_keys = []

    min_avgs, min_stds = {}, {}

    for i, exp_cfg in enumerate(exp_cfgs):
        if exp_cfg.exploration.explorer.ex_1.learner.m_disturb in ds:

            batch = jobfactory.make_jobgroup([exp_cfg])
            os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

            results_hub = hub.ResultsHub(batch, kind=kind)
            data = results_hub.data()[0]

            d = exp_cfg.exploration.explorer.ex_1.learner.m_disturb
            p = exp_cfg.exploration.explorer.weights[1][0]

            for N in Ns:
                env = exp_cfg.exp.env_name
                index = data['ticks'].index(N)
                env_key = (env, d, N)
                ps[env_key].append(p)
                avgs[env_key][p] = data['avg'][index]
                stds[env_key][p] = data['std'][index]
                if p == 0:
                    env_keys.append(env_key)

            for t in data['ticks']:
                env_name = exp_cfg.exp.env_name
                env_key = (env_name, d, t)
                min_avgs.setdefault(env_key, float('inf'))
                index = data['ticks'].index(t)
                if min_avgs[env_key] >= data['avg'][index]:
                    min_avgs[env_key] = data['avg'][index]
                    min_stds[env_key] = data['std'][index]

    for env_key in env_keys:
        ps[env_key] = sorted(ps[env_key])
        avgs[env_key] = np.array([avgs[env_key][p] for p in ps[env_key]])
        stds[env_key] = np.array([stds[env_key][p] for p in ps[env_key]])

    os.chdir(cwd)

    return env_keys, ps, avgs, stds, min_avgs, min_stds



if __name__ == '__main__':
    env_keys, ps, avgs, stds, min_avgs, min_stds = load_data('nn')

    colors = [graphs.BLUE, graphs.PINK, graphs.GREEN]
    graphs.output_file('c4_fig4_2_mbratio_perf.html')

    env_displayed = [env_key for env_key in env_keys if env_key[0] == 'kin20_150' and env_key[2] == 10000]

    for color, envd in zip(colors, env_displayed):
        print(avgs[envd])
        y_max = max(avgs[envd] + stds[envd])
        graphs.perf_std_discrete(ps[envd], avgs[envd], stds[envd], std_width=0.0035, color=color,
                                 y_range=[0.0, y_max+0.02], plot_width=1000, plot_height=500, title='{} {}'.format(*envd))
        graphs.hold(True)

    graphs.show()
