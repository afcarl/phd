# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../../c2/mesh')))

import numpy as np

from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

from fig3_8_unreach_graph import ratios, avgs, stds, ticks
from fig4_9_adapt_reach_cluster import expcfgs_levels, windows

Ns = ticks
W = 50

cwd = os.getcwd()
adapt_avgs = {}
adapt_stds = {}

for i, exp_cfg in enumerate(expcfgs_levels[0]):
    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

    data = hub.ResultsHub(batch, kind='nn').data()[0]
    window = exp_cfg.exploration.explorer.ex_1.window
    for N in Ns:
        index = data['ticks'].index(N)
        adapt_avgs[(window, N)] = data['avg'][index]
        adapt_stds[(window, N)] = data['std'][index]

os.chdir(cwd)

for N in Ns:
    for w in windows:
        print('N={}, w={} :  {} +- {}'.format(N, w, adapt_avgs[(w, N)], adapt_stds[(w, N)]))
    print()

if __name__ == '__main__':
    graphs.output_file('c4_fig4_9_adapt_reach_graph.html')
    for N in Ns:
        y_max = max(np.array(avgs[N]) + np.array(stds[N]))

        graphs.perf_std_discrete(ratios[N], avgs[N], stds[N], std_width=0.25, alpha=0.5,
                                 y_range=[0, y_max*1.05], title='adaptative reach performance, t = {}'.format(N))

        graphs.hold(True)
        graphs.line([0, 100], adapt_avgs[(W, N)], adapt_stds[(W, N)])
        graphs.hold(False)

    graphs.show()
