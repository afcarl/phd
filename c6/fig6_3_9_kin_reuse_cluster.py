# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os

import explib
import environments

import dotdot
import paths
import factored
import exs
import envs


DIM  = 20
MB_STEPS = 50

cfg = explib.desc._deepcopy()
cfg._update(paths.cfg)

cfg.meta.run_exploration = True
cfg.meta.run_tests       = False
cfg.meta.run_nns         = False
cfg.meta.run_coverage    = True

cfg.exp.path              = 'phd/c5/kin_reuse'
cfg.exp.prefix_name       = ('kin_reuse',)
cfg.exp.repetitions       = 100
cfg.exp.seeds.exploration = factored.seeds
cfg.job.steps             = 5000

cfg.testscov.buffer_size   = 0.05
cfg.testscov.ticks         = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]


env9_cfg = environments.envs.KinematicArm2D.defcfg._deepcopy()
env9_cfg.dim = DIM
env9_cfg.lengths = [0.9**i for i in range(env9_cfg.dim)]
env9_cfg.lengths = [s/sum(env9_cfg.lengths) for s in env9_cfg.lengths]
envs.catalog['kin20_150_0.9'] = env9_cfg

expcfgs_levels = [[], []]

src_cases = [('kin20_150',     'random.motor'),
             ('kin20_150',     'random.goal_4500'),
             ('kin20_150',     'random.goal_{}'.format(MB_STEPS)),
             ('kin20_150_0.9', 'random.goal_{}'.format(MB_STEPS))
            ]
for env_name, ex_name in src_cases:
    exp_cfg = cfg._deepcopy()
    if ex_name == 'random.goal_49000':
        exp_cfg.job.steps = 50000

    exp_cfg.exploration.explorer._update(exs.catalog[ex_name], overwrite=False)
    exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

    exp_cfg.exp.key = ((exp_cfg.exp.prefix_name + (ex_name, env_name), cfg.exp.repetitions), ())
    exp_cfg.exp.explorer_name = ex_name
    exp_cfg.exp.env_name      = env_name
    expcfgs_levels[0].append(exp_cfg)


for src_cfg in expcfgs_levels[0]:
    for algorithm in ['sensor_uniform', 'random']:
        for steps in [MB_STEPS, 500]:
            if src_cfg.exp.env_name == 'kin20_150':
                env_name = 'kin20_150_0.9'
                ex_name, ex_cfg = exs.reuse_explorer(steps, 1.0, 0.05, 20, algorithm=algorithm)
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
