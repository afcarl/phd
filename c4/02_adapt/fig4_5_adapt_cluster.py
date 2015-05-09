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

import fig4_4_adapt_ex

expcfgs_levels = [[]]
#THRESHOLDS = [0.01, 0.02, 0.05, 0.1]
THRESHOLDS = [0.02]

for THRESHOLD in THRESHOLDS:

    cfg = explib.desc._deepcopy()
    cfg._update(paths.cfg)

    cfg.meta.run_tests = False
    cfg.meta.run_nns   = True

    cfg.exp.path              = 'phd/c3/adapt'
    cfg.exp.prefix_name       = ('adapt{}'.format(THRESHOLD),)
    cfg.exp.repetitions       = 25
    cfg.exp.seeds.exploration = factored.seeds
    cfg.job.steps             = 10000

    cfg.testsetnn.testset_name = 'kin_one'
    cfg.testsetnn.algorithm    = 'fromfile'
    cfg.testsetnn.input_file   = paths.testset_filepath
    cfg.testsnn.ticks          = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

    cfg.testscov.buffer_size   = 0.02
    cfg.testscov.ticks         = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]



    env_names = ['kin20_150']

    for disturb in [0.001, 0.05, 0.5]: #0.025, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]:
        for env_name in env_names:
            exp_cfg = cfg._deepcopy()

            exp_cfg.exploration.explorer._update(fig4_4_adapt_ex.ex_cfg._deepcopy(), overwrite=False)
            exp_cfg.exploration.explorer.ex_1.learner.m_disturb = disturb
            explorer_name = 'adapt{}_{}_{}'.format(disturb, exp_cfg.exploration.explorer.window, THRESHOLD)

            exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

            exp_cfg.exp.prefix_name += (str(disturb),)
            exp_cfg.exp.key = ((exp_cfg.exp.prefix_name + (explorer_name, env_name), cfg.exp.repetitions), exp_cfg.exp.deps)
            exp_cfg.exp.explorer_name = explorer_name
            exp_cfg.exp.env_name      = env_name
            expcfgs_levels[0].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])
