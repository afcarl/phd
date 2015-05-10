# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os

import explib

import dotdot
import paths
import factored
import exs
import envs


cfg = explib.desc._deepcopy()
cfg._update(paths.cfg)

cfg.meta.run_exploration = True
cfg.meta.run_tests       = False
cfg.meta.run_nns         = False
cfg.meta.run_coverage    = True

cfg.exp.path              = 'phd/c2.1/dov_explore'
cfg.exp.prefix_name       = ('dov_explore',)
cfg.exp.repetitions       = 100
cfg.exp.seeds.exploration = factored.seeds
cfg.job.steps             = 2000

cfg.testscov.buffer_size   = 45/2.0
cfg.testscov.ticks         = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]


expcfgs_levels = [[], []]

env_names = ['dov_ball45_0.s']

for env_name in env_names:
    for learner in ['nn']:
        for mb in [20, 50, 100, 200, 250, 300, 500]:
            ex_name = 'random.goal_{}'.format(mb)
            exp_cfg = cfg._deepcopy()

            exp_cfg.exploration.explorer._update(exs.catalog[ex_name], overwrite=False)
            if learner == 'lwlr':
                exp_cfg.exploration.explorer.weights=((1.0, 0.0), (0.1, 0.9))
                exp_cfg.exploration.explorer.ex_1.learner = exs.lwlr_cfg
                exp_cfg.exp.prefix_name = exp_cfg.exp.prefix_name + (learner,)
            exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

            exp_cfg.exp.key = ((exp_cfg.exp.prefix_name + (ex_name, env_name), cfg.exp.repetitions), ())
            exp_cfg.exp.explorer_name = ex_name
            exp_cfg.exp.env_name      = env_name
            expcfgs_levels[0].append(exp_cfg)

if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])

