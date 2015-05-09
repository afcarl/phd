# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os

import numpy as np

from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

from fig4_2_mbratio_graph import load_data, disturbs
from fig4_5_adapt_cluster import expcfgs_levels, cfg


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
    window    = exp_cfg.exploration.explorer.window
    d         = exp_cfg.exploration.explorer.ex_1.learner.m_disturb

    # for N in cfg.testsnn.ticks:
    for N in Ns:
        index = data['ticks'].index(N)
        adapt_avgs[(d, N)] = data['avg'][index]
        adapt_stds[(d, N)] = data['std'][index]

os.chdir(cwd)


for d in disturbs:
    for N in Ns:
        print('N={}:  {} +- {}'.format(N, adapt_avgs[(d, N)], adapt_stds[(d, N)]))



if __name__ == '__main__':
    graphs.output_file('c4_fig4_5_adapt_graph_{}.html'.format(KIND))
    y_ranges=[(0.075, 0.3), (0.0, 0.1), (0.08, 0.14)]

    for i, d in enumerate(disturbs):
        y_range = y_ranges[i]
        for N in Ns:
            graphs.perf_std_discrete([100*i*0.05 for i in range(21)],
                                     avgs[('kin20_150', d, N)], stds[('kin20_150', d, N)],
                                     std_width=0.25, alpha=0.5, y_range=y_range,
                                     plot_height=300, title='d={} t={}'.format(d, N))
            graphs.hold(True)
            graphs.line([0, 100], adapt_avgs[(d, N)], adapt_stds[(d, N)])
            graphs.hold(False)

    graphs.show()
