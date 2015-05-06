import os
import math

import numpy as np
from bokeh import plotting

from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

from fig3_14_inverse_cluster import expcfgs_levels, cfg, env_names


exp_cfgs = expcfgs_levels[0]
cwd = os.getcwd()

steps = cfg.job.steps
disturb = {env: [] for env in env_names}
avgs    = {env: {} for env in env_names}
stds    = {env: {} for env in env_names}
y_max = 0.0

for i, exp_cfg in enumerate(exp_cfgs):
    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

    results_hub = hub.ResultsHub(batch, kind='nn')
    src_data = results_hub.data()
    assert len(src_data) == 1

    env_name = exp_cfg.exp.env_name
    n_motor  = exp_cfg.exploration.explorer.eras[0]
    env = env_name

    d = exp_cfg.exploration.explorer.ex_1.learner.m_disturb
    try:
        disturb[env].append(d)
        avgs[env][d] = src_data[0]['avg'][-1]
        stds[env][d] = src_data[0]['std'][-1]
    except ValueError:
        pass

env_displayed = ['kin2_150', 'kin7_150', 'kin20_150']

for env_name in env_displayed:
    disturb[env_name] = sorted(disturb[env_name])
    avgs[env_name] = np.array([avgs[env_name][d] for d in disturb[env_name]])
    stds[env_name] = np.array([stds[env_name][d] for d in disturb[env_name]])
    y_max = max(y_max, max(avgs[env_name] + stds[env_name]))
    print(y_max)

os.chdir(cwd)
colors = ['#2577B2', '#E84A5F']
plotting.output_file('../../../results/c3_fig3_14_inverse_perf.html')

for env_name in env_displayed:
    print(disturb[env_name])
    x = [math.log(d) for d in disturb[env_name]]
    graphs.bokeh_std_discrete(x, avgs[env_name], stds[env_name], std_width=0.02,
                              y_range=[0.0, 0.3], plot_width=1000, plot_height=300, title=str(env_name))
    plotting.hold(True)
    plotting.xaxis().minor_tick_line_color = None
    plotting.grid().grid_line_color = None
    plotting.xaxis().minor_tick_out = 0
    plotting.hold(False)

plotting.show()

