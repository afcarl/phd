import os

from bokeh import plotting

from explib.graphs import hub
from explib.jobs import jobfactory

from fig3_3_eval_cluster import expcfgs_levels

import dotdot
import graphs

dims, avgs, stds = {}, {}, {}
y_max = 0.0
cwd = os.getcwd()

displayed_dims = [2, 5, 7, 10, 15, 20, 30, 40, 60, 80, 100] #, 500, 1000]#, 2000]

for i, exp_cfg in enumerate(expcfgs_levels[0]):
    dim     = exp_cfg.job.env.dim

    if dim in displayed_dims:
        batch = jobfactory.make_jobgroup([exp_cfg])
        os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

        results_hub = hub.ResultsHub(batch, kind='cov')
        data = results_hub.data()[0]

        ex_name = exp_cfg.exp.explorer_name

        dims.setdefault(ex_name, [])
        avgs.setdefault(ex_name, [])
        stds.setdefault(ex_name, [])

        dims[ex_name].append(dim)
        avgs[ex_name].append(data['avg'][-1])
        stds[ex_name].append(data['std'][-1])
        y_max = max(y_max, data['avg'][-1] + data['std'][-1])


os.chdir(cwd)
colors = ['#2577B2', '#E84A5F']
plotting.output_file('../../../results/c3_fig3_3_eval_perf.html')

for color, ex_name in zip(colors, dims.keys()):
    graphs.bokeh_std_discrete(dims[ex_name], avgs[ex_name], stds[ex_name], std_width=0.25, color=color,
                              x_range=[0.0, 110.0], y_range=[0.0, y_max+0.1],
                              plot_width=1000, plot_height=300, title=str(ex_name))
    plotting.hold(True)

plotting.show()
