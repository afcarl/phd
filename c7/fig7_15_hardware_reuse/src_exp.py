import os

import explib

import dotdot
import paths
import exsh as exs
import envs


suffix = 'h'
cfg = explib.desc._deepcopy()
cfg._update(paths.cfg)

cfg.meta.run_nns      = False
cfg.meta.run_coverage = True

explorer_roaster = ['src_expl']

cfg.exp.path        = 'icdl2014'
cfg.exp.prefix_name = ['icdl2014']
cfg.exp.repetitions = 4
cfg.job.steps       = 1000

cfg.testscov.buffer_size = 45/2.0
cfg.testscov.ticks       = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, cfg.job.steps+1, 25)]

# cfg.testsetnn.testset_name = 'icdl2014'
# cfg.testsetnn.size         = 400
# cfg.testsetnn.algorithm    = 'random.sensory'

# cfg.testsnn.ticks  = [1, 2, 3, 4, 5, 10, 15, 20] + [25*(i+1) for i in range(10*4)]

# cfg.testset.testset_name = 'icdl2014'
# cfg.testset.size         = 100
# cfg.testset.algorithm    = 'random.sensory'

# cfg.tests.ticks = [1, 2, 3, 5, 10, 15, 25, 50] + [100*(i+1) for i in range(10)]
# cfg.tests.rep   = 3
# cfg.tests.explorer.learner = expl.learn_cfg


src_envs = ('ball45_0_a20.' + suffix, 'cube45_0_a20.' + suffix)
expcfgs_levels = [[]]

for explorer_name in explorer_roaster:
    for env_name in src_envs:
        exp_cfg = cfg._deepcopy()

        exp_cfg.exploration.explorer._update(exs.catalog[explorer_name], overwrite=False)
        exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)
        exp_cfg.job.env.execute.simu.verbose = False
        #exp_cfg.job.env.execute.simu.ppf        = 1
        #exp_cfg.job.env.execute.simu.headless   = False

        exp_cfg.exp.key = ((tuple(exp_cfg.exp.prefix_name) + (explorer_name, env_name), cfg.exp.repetitions), exp_cfg.exp.deps)
        exp_cfg.exp.explorer_name = explorer_name
        exp_cfg.exp.env_name      = env_name
        expcfgs_levels[0].append(exp_cfg)

if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])



