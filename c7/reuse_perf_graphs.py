# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os, sys
import importlib
import copy


from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

# import exp description
# module_name = sys.argv[1][:-3]
# module = importlib.import_module(module_name)
# expcfgs = module.expcfgs
# MB_STEPS = module.MB_STEPS



def listit(t):
    return list(map(listit, t)) if isinstance(t, (list, tuple)) else t

def tupleit(t):
    return tuple(map(tupleit, t)) if isinstance(t, (list, tuple)) else t

def randomit(key):
    key = copy.deepcopy(key)
    key = listit(key)
    key[0][0][-2] = 'reuse.random' + key[0][0][-2][5:]
    return tupleit(key)

def load_results(exp_cfgs):
    exp_cfgs = exp_cfgs[0] + exp_cfgs[1]

    sources, targets = {}, {}
    for i, exp_cfg in enumerate(exp_cfgs):
        cwd = os.getcwd()

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
            if len(src_data[0]['avg']) == 0:
                print('MISSING: {}'.format(exp_cfg.exp.key))
            else:
                targets[exp_cfg.exp.key] = results

        os.chdir(cwd)

    return sources, targets



def perf_graphs(sources, targets, mb_steps=200, y_maxs=(360000, 200000)):
    already = False

    for (env_name, ex_name), results in targets.items():
        exp_cfg = results['exp_cfg']

        if not exp_cfg.exp.explorer_name.startswith('reuse.random'):

            if len(exp_cfg.exp.key[1]) != 0:
                if not already:
                    already = False
                    src_results = sources[(exp_cfg.exp.env_name, 'random.goal_{}'.format(mb_steps))]
                    y_max = y_maxs[0] if exp_cfg.exp.env_name.startswith('dov_ball') else y_maxs[1]
                    graphs.perf_astd(src_results['ticks'], src_results['avg'], src_results['astd'],
                                     color=graphs.NOREUSE_COLOR, plot_width=1000, plot_height=500,
                                     x_range=(0, exp_cfg.job.steps), y_range=(0, y_max),
                                     title='{}'.format(exp_cfg.exp.key))
                    graphs.hold(True)

                print('{}::{} {}'.format(exp_cfg.exp.env_name, exp_cfg.exp.explorer_name, results['avg'][-1]))
                graphs.bokeh_astds(results['ticks'], results['avg'], results['astd'],
                                   color=graphs.REUSE_COLOR)
                graphs.hold(True)

                random_key = randomit(exp_cfg.exp.key)
                if random_key in targets:
                    random_results = targets[random_key]
                    graphs.perf_astd(random_results['ticks'], random_results['avg'], random_results['astd'],
                                    color=graphs.RANDREUSE_COLOR)

                graphs.hold(False)
