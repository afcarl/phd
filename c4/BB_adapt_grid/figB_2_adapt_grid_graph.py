import os

import numpy as np

from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

from fig4_2_mbratio_graph import load_data, disturbs
from figB_2_adapt_grid_cluster import expcfgs_levels, cfg, RESS


RESS = [20, 40]
Ns = [10000]
KIND = 'nn'

mbratio_env_keys, ps, avgs, stds, min_avgs, min_stds = load_data(KIND)

cwd = os.getcwd()
adapt_avgs = {}
adapt_stds = {}

for i, exp_cfg in enumerate(expcfgs_levels[0]):
    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

    data = hub.ResultsHub(batch, kind=KIND).data()[0]
    res = exp_cfg.exploration.explorer.res
    d   = exp_cfg.exploration.explorer.ex_1.learner.m_disturb

    # for N in cfg.testsnn.ticks:
    for N in Ns:
        index = data['ticks'].index(N)
        adapt_avgs[(d, res, N)] = data['avg'][index]
        adapt_stds[(d, res, N)] = data['std'][index]

os.chdir(cwd)


# for d in disturbs:
#     for N in Ns:
#         print('N={}:  {} +- {}'.format(N, adapt_avgs[(d, res, N)], adapt_stds[(d, res N)]))



if __name__ == '__main__':
    graphs.output_file('c4_fig4_5_adapt_graph_{}.html'.format(KIND))
    y_ranges=[(0.075, 0.3), (0.0, 0.1), (0.08, 0.14)]

    for i, d in enumerate(disturbs):
        y_range = y_ranges[i]
        for N in Ns:
            for res in RESS:
                graphs.perf_std_discrete([100*i*0.05 for i in range(21)], avgs[('kin20_150', d, N)], stds[('kin20_150', d, N)],
                                         std_width=0.25, color='#2577B2', alpha=0.5,
                                         y_range=y_range, #y_range=[y_min-0.1, y_max+0.1],
                                         plot_width=1000, plot_height=300, title='d={} t={} res={}'.format(d, N, res))

                graphs.hold(True)
                graphs.line([0, 100], adapt_avgs[(d, res, N)], adapt_stds[(d, res, N)])
                graphs.hold(False)

    graphs.show()
