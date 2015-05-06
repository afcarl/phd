import os

import explib

import dotdot
import paths
import factored
import envs
import exs

cfg = explib.desc._deepcopy()
cfg._update(paths.cfg)

cfg.meta.run_tests    = False
cfg.meta.run_nns      = True
cfg.meta.run_coverage = True

cfg.exp.path              = 'phd/c2/eval'
cfg.exp.prefix_name       = ('eval',)
cfg.exp.repetitions       = 25
cfg.exp.seeds.exploration = factored.seeds
cfg.job.steps             = 10000

cfg.testsetnn.testset_name = 'kin_one'
cfg.testsetnn.algorithm    = 'fromfile'
cfg.testsetnn.input_file   = paths.testset_filepath
cfg.testsnn.ticks          = [2000, 10000] #[1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

cfg.testscov.buffer_size   = 0.02
cfg.testscov.ticks         = [2000, 10000] #[1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

expcfgs_levels = [[]]

for dim in [2, 5, 7, 8, 9, 10, 15, 20, 30, 40, 60, 80, 100] : #, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000]:
    for explorer_name in ['random.motor', 'random.goal']:
        env_name = 'kin{}_150'.format(dim)
        exp_cfg = cfg._deepcopy()

        exp_cfg.exploration.explorer._update(exs.catalog[explorer_name], overwrite=False)
        exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

        exp_cfg.exp.key = ((exp_cfg.exp.prefix_name + (explorer_name, env_name), cfg.exp.repetitions), ())
        exp_cfg.exp.explorer_name = explorer_name
        exp_cfg.exp.env_name      = env_name
        expcfgs_levels[0].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])
