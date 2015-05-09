# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import explib

import dotdot
import paths
import factored
import exs
import envs


RES = 40

cfg = explib.desc._deepcopy()
cfg._update(paths.cfg)

cfg.meta.run_tests    = False
cfg.meta.run_nns      = True
cfg.meta.run_coverage = False

cfg.exp.path              = 'phd/c2/unreach'
cfg.exp.prefix_name       = ['unreach' if RES == 20 else 'unreach{}'.format(RES)]
cfg.exp.repetitions       = 50
cfg.exp.seeds.exploration = factored.seeds
cfg.job.steps             = 10000

cfg.testsetnn.testset_name = 'kin_one'
cfg.testsetnn.algorithm    = 'fromfile'
cfg.testsetnn.input_file   = paths.testset_filepath
cfg.testsnn.ticks          = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

src_envs      = ('kin20_150',)
src_explorers = ['unreach_{}'.format(r) for r in range(0, 101, 5)]

expcfgs_levels = [[]]
for explorer_name in src_explorers:
    for env_name in src_envs:
        exp_cfg = cfg._deepcopy()

        ex_cfg = exs.catalog[explorer_name]._deepcopy()
        ex_cfg.ex_1.res = RES
        ex_cfg.ex_2.res = RES

        exp_cfg.exploration.explorer._update(exs.catalog[explorer_name], overwrite=False)
        exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

        exp_cfg.exp.key = ((tuple(exp_cfg.exp.prefix_name) + (explorer_name, env_name), cfg.exp.repetitions), exp_cfg.exp.deps)
        exp_cfg.exp.explorer_name = explorer_name
        exp_cfg.exp.env_name      = env_name
        expcfgs_levels[0].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])
