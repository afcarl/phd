# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os
import math


from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

from fig6_3_9_kin_reuse_cluster import expcfgs_levels, cfg

sem = 1.0 # cfg.exp.repetitions # if sem == rep then SEM instead of SD

cwd = os.getcwd()

exp_cfgs = expcfgs_levels[0]+expcfgs_levels[1]
sources, targets = {}, {}
for i, exp_cfg in enumerate(exp_cfgs):
    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

    results_hub = hub.ResultsHub(batch, kind='cov')
    src_data = results_hub.data()
    assert len(src_data) == 1

    results = {'exp_cfg': exp_cfg}
    results.update(src_data[0])

    if len(exp_cfg.exp.key[1]) == 0:
        sources[(exp_cfg.exp.env_name, exp_cfg.exp.explorer_name)] = results
    else:
        targets[exp_cfg.exp.key] = results


os.chdir(cwd)

sources_set = set([])

graphs.output_file('c5_kin_reuse_perf.html')
for (env_name, ex_name), results in targets.items():
    exp_cfg = results['exp_cfg']

    if len(exp_cfg.exp.key[1]) != 0:
        # source task
        src_ex_name = exp_cfg.exp.key[1][0][0][-2]
        src_env_name = exp_cfg.exp.key[1][0][0][-1]
        sources_set.add((src_env_name, src_ex_name))

        # no reuse
        nor_results = sources[(exp_cfg.exp.env_name, 'random.goal_50')]
        graphs.bokeh_astds(nor_results['ticks'], nor_results['avg'], nor_results['astd'],
                           color=graphs.NOREUSE_COLOR, plot_width=1000, plot_height=500, sem=sem,
                           x_range=(0, exp_cfg.job.steps), y_range=(0, math.pi),
                           title='{}'.format(exp_cfg.exp.key))
        graphs.hold(True)

        # if exp_cfg.exp.explorer_name.startswith('reuse.random'): # makes it actually harder to compare.
        #     tgt_color = graphs.RANDREUSE_COLOR
        print('{}::{} {}'.format(exp_cfg.exp.env_name, exp_cfg.exp.explorer_name, results['avg'][-1]))
        graphs.perf_astd(results['ticks'], results['avg'], results['astd'], sem=sem,
                         color=graphs.REUSE_COLOR)
        graphs.hold(False)

for (env_name, ex_name) in sources_set:
    src_results = sources[(env_name, ex_name)]
    exp_cfg = src_results['exp_cfg']
    graphs.perf_astd(src_results['ticks'], src_results['avg'], src_results['astd'],
                     color=graphs.NOREUSE_COLOR, plot_width=1000, plot_height=500, sem=sem,
                     x_range=(0, exp_cfg.job.steps), y_range=(0, math.pi), # should be 3.268 instead
                     title='{}'.format(exp_cfg.exp.key))
    graphs.hold(True)


graphs.show()
