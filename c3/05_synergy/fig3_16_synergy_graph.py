import os

from bokeh import plotting

from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

from fig3_16_synergy_cluster import expcfgs_levels


exp_cfgs = expcfgs_levels[0]

cwd = os.getcwd()

ticks, avgs, stds = [], [], []
for i, exp_cfg in enumerate(exp_cfgs):
    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

    results_hub = hub.ResultsHub(batch, kind='nn')
    src_data = results_hub.data()
    assert len(src_data) == 1

    ticks.append(src_data[0]['ticks'])
    avgs.append(src_data[0]['avg'])
    stds.append(src_data[0]['std'])

os.chdir(cwd)

colors = [graphs.SRC_COLOR, graphs.SRC_COLOR]
plotting.output_file('../../../results/c3_fig3_16_synergy_perf.html')
for color, tick, avg, std, exp_cfg in zip(colors, ticks, avgs, stds, exp_cfgs):
    print('{}::{} {}'.format(exp_cfg.exp.env_name, exp_cfg.exp.explorer_name, avg[-1]))
    graphs.bokeh_stds(tick, avg, std, color=color, plot_width=1000, plot_height=300,
                      x_range=(0, exp_cfg.job.steps), y_range=(0.0, 0.4),
                      legend='{} {}'.format(exp_cfg.exp.env_name, exp_cfg.exp.explorer_name))
    plotting.hold(True)
plotting.show()

