# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import explib
import explorers

import dotdot
import paths
import factored
import exs
import envs

import fig4_8_adapt_reach_ex


expcfgs_levels = [[]]
#THRESHOLDS = [0.01, 0.02, 0.05, 0.1]
THRESHOLDS = [0.02, 0.05, 0.1]
windows = [50]

cfg = explib.desc._deepcopy()
cfg._update(paths.cfg)

cfg.meta.run_tests    = False
cfg.meta.run_nns      = True
cfg.meta.run_coverage = False

cfg.exp.path              = 'phd/c3/adapt_reach'
cfg.exp.repetitions       = 50
cfg.exp.seeds.exploration = factored.seeds
cfg.job.steps             = 10000

cfg.testsetnn.testset_name = 'kin_one'
cfg.testsetnn.algorithm    = 'fromfile'
cfg.testsetnn.input_file   = paths.testset_filepath
cfg.testsnn.ticks          = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

# cfg.testscov.buffer_size   = 0.02
# cfg.testscov.ticks         = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

for THRESHOLD in THRESHOLDS:
    exp_cfg = cfg._deepcopy()
    env_name = 'kin20_150'

    # Explorer Config
    ex_cfg = fig4_8_adapt_reach_ex.ex_cfg._deepcopy()
    ex_cfg.ex_1.threshold = THRESHOLD
    explorer_name = 'adapt_reach{}_{}_{}'.format(ex_cfg.ex_1.ex_1.learner.m_disturb, ex_cfg.ex_1.window, THRESHOLD)

    exp_cfg.exp.prefix_name = ('adapt_reach{}'.format(THRESHOLD),)
    exp_cfg.exploration.explorer._update(ex_cfg, overwrite=False)
    exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

    exp_cfg.exp.key = ((exp_cfg.exp.prefix_name + (explorer_name, env_name), cfg.exp.repetitions), exp_cfg.exp.deps)
    exp_cfg.exp.explorer_name = explorer_name
    exp_cfg.exp.env_name      = env_name
    expcfgs_levels[0].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])
