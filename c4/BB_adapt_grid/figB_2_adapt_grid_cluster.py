import explib
import explorers

import dotdot
import paths
import factored
import exs
import envs

import fig4_4_adapt_ex

expcfgs_levels = [[]]
RESS = [20, 40]

for RES in RESS:

    cfg = explib.desc._deepcopy()
    cfg._update(paths.cfg)

    cfg.meta.run_tests    = False
    cfg.meta.run_nns      = True
    cfg.meta.run_coverage = False

    cfg.exp.path              = 'phd/c4/adapt_grid'
    cfg.exp.prefix_name       = ('adapt_grid{}'.format(RES),)
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

    # explorer Config
    ex_cfg  = fig4_4_adapt_ex.grid_cfg
    ex_cfg.res = RES

    for disturb in [0.001, 0.05, 0.5]: #0.025, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]:
        for env_name in env_names:
            exp_cfg = cfg._deepcopy()
            explorer_name = 'adapt_grid{}_{}_{}'.format(disturb, ex_cfg.window, RES)

            exp_cfg.exploration.explorer._update(ex_cfg._deepcopy(), overwrite=False)
            exp_cfg.exploration.explorer.ex_1.learner.m_disturb = disturb
            exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

            exp_cfg.exp.prefix_name += (str(disturb),)
            exp_cfg.exp.key = ((exp_cfg.exp.prefix_name + (explorer_name, env_name), cfg.exp.repetitions), exp_cfg.exp.deps)
            exp_cfg.exp.explorer_name = explorer_name
            exp_cfg.exp.env_name      = env_name
            expcfgs_levels[0].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])
