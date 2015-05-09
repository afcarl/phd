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

cfg.meta.run_exploration = False
cfg.meta.run_tests = False
cfg.meta.run_nns   = True

cfg.exp.path              = 'phd/c3/mbratio'
cfg.exp.prefix_name       = ('mbratio',)
cfg.exp.repetitions       = 25
cfg.exp.seeds.exploration = factored.seeds
cfg.job.steps             = 10000

cfg.testsetnn.testset_name = 'kin_one'
cfg.testsetnn.algorithm    = 'fromfile'
cfg.testsetnn.input_file   = paths.testset_filepath
cfg.testsnn.ticks          = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

cfg.testscov.buffer_size   = 0.02
cfg.testscov.ticks         = [1000*i for i in range(11)]


expcfgs_levels = [[]]
env_names = ['kin20_150']
disturbs = [0.001, 0.05, 0.5]
explorer_name = 'random.goal'

for disturb in disturbs:
    for p in [i*0.05 for i in range(21)]:
        for env_name in env_names:
            exp_cfg = cfg._deepcopy()

            exp_cfg.exploration.explorer._update(exs.catalog[explorer_name]._deepcopy(), overwrite=False)
            exp_cfg.exploration.explorer.weights                = ((1.0, 0.0), (p, 1-p))
            exp_cfg.exploration.explorer.eras                   = (1, None)
            exp_cfg.exploration.explorer.ex_1.learner.m_disturb = disturb

            exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)
            exp_cfg.exp.prefix_name += (str(disturb),str(p))
            exp_cfg.exp.key = ((exp_cfg.exp.prefix_name + (explorer_name, env_name), cfg.exp.repetitions), exp_cfg.exp.deps)
            exp_cfg.exp.explorer_name = explorer_name
            exp_cfg.exp.env_name      = env_name
            expcfgs_levels[0].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])
