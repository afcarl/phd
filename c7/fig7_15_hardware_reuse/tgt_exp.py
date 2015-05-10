import os

import explib

import dotdot
import paths
import exsh as exs
import envs

from src_exp import cfg, suffix
from src_exp import expcfgs_levels, src_envs


tgt_envs = [('ball45_0_a20.' + suffix, 'ball45_0_a20.' + suffix),
            ('ball45_0_a20.' + suffix, 'cube45_0_a20.' + suffix),
            ('cube45_0_a20.' + suffix, 'ball45_0_a20.' + suffix),
            ('cube45_0_a20.' + suffix, 'cube45_0_a20.' + suffix),
           ]

explorer_roaster = ['tgt_expl']

cfg = cfg._deepcopy()
cfg.exp.prefix_name = ['icdl2014']
cfg.exp.deps = ((('icdl2014', 'src_exp'), cfg.exp.repetitions),)


expcfgs_levels.append([])
for explorer_name in explorer_roaster:
    for src_env_name, env_name in tgt_envs:
        exp_cfg = cfg._deepcopy()
        if (src_env_name, env_name) == ('ball45_0_a20.h', 'cube45_0_a20.h'):
            exp_cfg.exp.repetitions = 3
        exp_cfg.exploration.explorer._update(exs.catalog[explorer_name], overwrite=False)
        exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

        exp_deps = ((('icdl2014', 'src_expl', src_env_name), cfg.exp.repetitions),)
        exp_cfg.exp.deps = exp_deps
        exp_cfg.exp.key = ((tuple(exp_cfg.exp.prefix_name) + ('src_expl', src_env_name, explorer_name, env_name), exp_cfg.exp.repetitions), exp_cfg.exp.deps)
        exp_cfg.exp.explorer_name = explorer_name
        exp_cfg.exp.env_name      = env_name
        expcfgs_levels[1].append(exp_cfg)


if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs_levels for cfg in cfg_level])



