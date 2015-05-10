# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os
import copy

import numpy as np

from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

from fig7_9_dov_sources_cluster import expcfgs_levels


exp_cfgs = expcfgs_levels[0]
tasks = {}

cwd = os.getcwd()
for i, exp_cfg in enumerate(exp_cfgs):
    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

    results_hub = hub.ResultsHub(batch, kind='cov')
    src_data = results_hub.data()
    assert len(src_data) == 1

    results = {'exp_cfg': exp_cfg}
    results.update(src_data[0])

    tasks[exp_cfg.exp.key] = results
os.chdir(cwd)


def listit(t):
    return list(map(listit, t)) if isinstance(t, (list, tuple)) else t

def tupleit(t):
    return tuple(map(tupleit, t)) if isinstance(t, (list, tuple)) else t

graphs.output_file('c7_fig7_9_sources_perf.html')
keys = sorted(tasks.keys())
for key in keys:

    results = tasks[key]
    exp_cfg = results['exp_cfg']
    explorer_name = exp_cfg.exp.explorer_name
    env_name = exp_cfg.exp.env_name

    if 'lwlr' not in exp_cfg.exp.key[0][0] and exp_cfg.exp.key[0][0][-1].find('a20.') == -1:
        graphs.perf_astd(results['ticks'], results['avg'], results['astd'],
                         color=graphs.NOREUSE_COLOR, plot_width=1000, plot_height=500,
                         x_range=(0, 2000), y_range=(0, 360000),
                         title='{}'.format(results['exp_cfg'].exp.key))

graphs.show()
