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


MB_STEPS = 300

cfg = explib.desc._deepcopy()
cfg._update(paths.cfg)

cfg.meta.run_tests    = False
cfg.meta.run_nns      = False
cfg.meta.run_coverage = True

cfg.exp.path              = 'phd/c6/dov_reuse'
cfg.exp.prefix_name       = ('dov_reuse', 'lwlr')
cfg.exp.repetitions       = 25
cfg.exp.seeds.exploration = factored.seeds
cfg.job.steps             = 1000

cfg.testscov.buffer_size   = 45/2.0
cfg.testscov.ticks         = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]


exps = [('dov_ball45_0_a20.s', 'dov_ball45_0_a20.s'),
        ('dov_ball45_0_a20.s', 'dov_cube45_0_a20.s'),
        ('dov_cube45_0_a20.s', 'dov_cube45_0_a20.s'),
        ('dov_cube45_0_a20.s', 'dov_ball45_0_a20.s'),
        # ('dov_ball45_0_a20.s', 'dov_ball45_1_a20.s'), # misreuse
        # ('dov_ball45_1_a20.s', 'dov_ball45_0_a20.s'), # misreuse
       ]
src_exps = set([e  for e, _ in exps] + [e  for _, e in exps])

expcfgs_levels = [[], []]

for env_name in src_exps:
    ex_names = ['random.goal_{}'.format(MB_STEPS)]
#    ex_names = ['random.goal_{}'.format(MB_STEPS), 'random.motor']

    for ex_name in ex_names:
        exp_cfg = cfg._deepcopy()

        exp_cfg.exploration.explorer._update(exs.catalog[ex_name], overwrite=False)
        if ex_name.startswith('random.goal'):
            exp_cfg.exploration.explorer.weights=((1.0, 0.0), (0.1, 0.9))
            exp_cfg.exploration.explorer.ex_1.learner = exs.lwlr_cfg
        exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

        exp_cfg.exp.key = ((exp_cfg.exp.prefix_name + (ex_name, env_name), cfg.exp.repetitions), ())
        exp_cfg.exp.explorer_name = ex_name
        exp_cfg.exp.env_name      = env_name
        expcfgs_levels[0].append(exp_cfg)


for src_cfg in expcfgs_levels[0]:

    env_names = [e for d, e in exps if d == src_cfg.exp.env_name]
    algorithms = ['sensor_uniform']
    algorithms = ['sensor_uniform', 'random']

    for env_name in env_names:
        for algorithm in algorithms:
            ex_name, ex_cfg = exs.reuse_explorer(MB_STEPS, 0.5, 0.05, 40, algorithm=algorithm)
            ex_cfg.weights=((0.5, 0.5, 0.0), (0.05, 0.05, 0.9))
            ex_cfg.ex_2.learner = exs.lwlr_cfg

            exp_cfg = cfg._deepcopy()

            exp_cfg.exploration.explorer = ex_cfg
            exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

            exp_cfg.exp.deps = (src_cfg.exp.key[0],)
            exp_cfg.exp.key = ((tuple(exp_cfg.exp.prefix_name) + (src_cfg.exp.explorer_name, src_cfg.exp.env_name, ex_name, env_name), cfg.exp.repetitions), exp_cfg.exp.deps)
            exp_cfg.exp.explorer_name = ex_name
            exp_cfg.exp.env_name      = env_name
            expcfgs_levels[1].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])


