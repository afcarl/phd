import os

import explib

import dotdot
import paths
import factored
import exs
import envs


cfg = explib.desc._deepcopy()
cfg._update(paths.cfg)

cfg.meta.run_coverage = False
cfg.meta.run_tests    = False
cfg.meta.run_nns      = True

cfg.exp.path              = 'phd/c2/synergy/'
cfg.exp.prefix_name       = ['synergy']
cfg.exp.repetitions       = 25
cfg.exp.seeds.exploration = factored.seeds
cfg.job.steps             = 10000

cfg.testsetnn.testset_name = 'kin_one'
cfg.testsetnn.algorithm    = 'fromfile'
cfg.testsetnn.input_file   = paths.testset_filepath
cfg.testsnn.ticks          = [10000] #1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

expcfgs_levels = [[]]
for explorer_name in ['random.motor', 'random.goal']:
    for env_name in ['kin20_150', 'kinsyn20_2']:
        exp_cfg = cfg._deepcopy()

        exp_cfg.exploration.explorer._update(exs.catalog[explorer_name], overwrite=False)
        exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

        exp_cfg.exp.key = ((tuple(exp_cfg.exp.prefix_name) + (explorer_name, env_name), cfg.exp.repetitions), exp_cfg.exp.deps)
        exp_cfg.exp.explorer_name = explorer_name
        exp_cfg.exp.env_name      = env_name
        expcfgs_levels[0].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])
