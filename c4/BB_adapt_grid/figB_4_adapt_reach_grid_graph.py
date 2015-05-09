import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../../c3/03_grid')))

import numpy as np

from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

from fig3_8_unreach_graph import ratios, avgs, stds
from figB_4_adapt_reach_grid_cluster import expcfgs_levels, windows, RESS


#Ns = [100, 1000, 2000, 5000, 10000]
Ns = [2000, 10000]
W = windows[0]

cwd = os.getcwd()
adapt_avgs = {}
adapt_stds = {}

for i, exp_cfg in enumerate(expcfgs_levels[0]):
    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

    data = hub.ResultsHub(batch, kind='nn').data()[0]
    window = exp_cfg.exploration.explorer.ex_1.window
    res    = exp_cfg.exploration.explorer.ex_1.res
    for N in Ns:
        print(data['ticks'])
        index = data['ticks'].index(N)
        adapt_avgs[(window, N, res)] = data['avg'][index]
        adapt_stds[(window, N, res)] = data['std'][index]

os.chdir(cwd)

# for N in Ns:
#     for w in windows:
#         print('N={}, w={} :  {} +- {}'.format(N, w, adapt_avgs[(w, N, 20)], adapt_stds[(w, N, 20)]))
#     print()

if __name__ == '__main__':
    graphs.output_file('c4_figB_4_adaptg_reach_graph.html')
    for res in RESS:
        for N in Ns:
            y_max = max(np.array(avgs[N]) + np.array(stds[N]))

            graphs.perf_std_discrete(ratios[N], avgs[N], stds[N], color='#2577B2', alpha=0.5,
                                     y_range=[0, y_max*1.05], title='adaptg_reach, t={}, res={}'.format(N, res),
                                     std_width=0.25, plot_width=1000, plot_height=300)

            graphs.hold(True)
            graphs.line([0, 100], adapt_avgs[(W, N, res)], adapt_stds[(W, N, res)])
            graphs.hold(False)

    graphs.show()
