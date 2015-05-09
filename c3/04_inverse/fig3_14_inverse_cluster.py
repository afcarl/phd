# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import explib

import dotdot
import paths
import factored
import exs
import envs


cfg = explib.desc._deepcopy()
cfg._update(paths.cfg)

cfg.meta.run_tests    = False
cfg.meta.run_nns      = True
cfg.meta.run_coverage = False

cfg.exp.path              = 'phd/c3/inverse'
cfg.exp.prefix_name       = ('inverse',)
cfg.exp.repetitions       = 100
cfg.exp.seeds.exploration = factored.seeds
cfg.job.steps             = 10000

cfg.testsetnn.testset_name = 'kin_one'
cfg.testsetnn.algorithm    = 'fromfile'
cfg.testsetnn.input_file   = paths.testset_filepath
cfg.testsnn.ticks          = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

expcfgs_levels = [[]]


env_names = ['kin2_150', 'kin7_150', 'kin20_150']
ex_name = 'random.goal'

for p in [0.001, 0.025, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]:
    for env_name in env_names:
        exp_cfg = cfg._deepcopy()

        exp_cfg.exploration.explorer._update(exs.catalog[ex_name], overwrite=False)
        exp_cfg.exploration.explorer.ex_1.learner.m_disturb = p
        exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

        exp_cfg.exp.prefix_name += (str(p),)
        exp_cfg.exp.key = ((exp_cfg.exp.prefix_name + (ex_name, env_name), cfg.exp.repetitions), exp_cfg.exp.deps)
        exp_cfg.exp.explorer_name = ex_name
        exp_cfg.exp.env_name      = env_name
        expcfgs_levels[0].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])
