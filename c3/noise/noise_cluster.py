import explib

import dotdot
import paths
import factored
import envs
import exs


cfg = explib.desc._deepcopy()
cfg._update(paths.cfg)

cfg.meta.run_tests = False
cfg.meta.run_nns   = True

cfg.exp.path              = 'phd/c3/noise'
cfg.exp.prefix_name       = ['noise']
cfg.exp.repetitions       = 10
cfg.exp.seeds.exploration = factored.seeds
cfg.job.steps             = 10000

cfg.testsetnn.testset_name = 'kin_one'
cfg.testsetnn.algorithm    = 'fromfile'
cfg.testsetnn.input_file   = paths.testset_filepath
cfg.testsnn.ticks          = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

env_name = 'kin20_150'
ex_name  = 'goal.random'


expcfgs_levels = [[]]
for s_noise in [0, 0.01, 0.02, 0.05, 0.1, 0.5, 1.0]:
    exp_cfg = cfg._deepcopy()
    exp_cfg.exp.s_noise = s_noise

    exp_cfg.exploration.explorer._update(exs.catalog[ex_name], overwrite=False)
    exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

    exp_cfg.exp.key = ((tuple(exp_cfg.exp.prefix_name) + ('s_noise{}'.format(s_noise), ex_name, env_name), cfg.exp.repetitions), ())
    exp_cfg.exp.ex_name  = ex_name
    exp_cfg.exp.env_name = env_name
    expcfgs_levels[0].append(exp_cfg)

for m_noise in [0, 0.01, 0.02, 0.05, 0.1, 0.5, 1.0]:
    exp_cfg = cfg._deepcopy()
    exp_cfg.exp.m_noise = m_noise

    exp_cfg.exploration.explorer._update(exs.catalog[ex_name], overwrite=False)
    exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

    exp_cfg.exp.key = ((tuple(exp_cfg.exp.prefix_name) + ('m_noise{}'.format(s_noise), ex_name, env_name), cfg.exp.repetitions), ())
    exp_cfg.exp.ex_name  = ex_name
    exp_cfg.exp.env_name = env_name
    expcfgs_levels[0].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])
