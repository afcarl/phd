# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os


from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs

from tgt_exp import expcfgs_levels


cwd = os.getcwd()

exp_cfgs = expcfgs_levels[0] + expcfgs_levels[1]
sources, targets = {}, {}
for i, exp_cfg in enumerate(exp_cfgs):
    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath)[:-1]+'.hard')

    results_hub = hub.ResultsHub(batch, kind='cov')
    src_data = results_hub.data()
    assert len(src_data) == 1

    results = {'exp_cfg': exp_cfg}
    results.update(src_data[0])

    if len(exp_cfg.exp.key[1]) == 0:
        sources[(exp_cfg.exp.key[0][0][0], exp_cfg.exp.env_name, exp_cfg.exp.explorer_name)] = results
    else:
        targets[exp_cfg.exp.key] = results


os.chdir(cwd)

graphs.output_file('c7_fig7_15_dov_reuse_hard_perf.html')
for (env_name, ex_name), results in targets.items():
    exp_cfg = results['exp_cfg']
    print(exp_cfg.exp.key)

    if len(exp_cfg.exp.key[1]) != 0:
        src_results = sources[(exp_cfg.exp.key[0][0][0], exp_cfg.exp.env_name, 'src_expl')]
        y_max = 1000000 if exp_cfg.exp.env_name.startswith('ball') else 400000
        print(max(src_results['ticks']))
        graphs.bokeh_astds(src_results['ticks'], src_results['avg'], src_results['astd'],
                           color=graphs.NOREUSE_COLOR, plot_width=1000, plot_height=500,
                           x_range=(0, exp_cfg.job.steps), y_range=(0, y_max),
                           title='{}'.format(exp_cfg.exp.key))
        graphs.hold(True)

        print('{}::{} {}'.format(exp_cfg.exp.env_name, exp_cfg.exp.explorer_name, results['avg'][-1]))
        graphs.bokeh_astds(results['ticks'], results['avg'], results['astd'],
                           color=graphs.REUSE_COLOR)
        graphs.hold(False)

graphs.show()
