# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os

import explib

import dotdot
import paths
import factored
import exs
import envs


MB_STEPS = 200

_cfg = explib.desc._deepcopy()
_cfg._update(paths.cfg)

_cfg.meta.run_tests    = False
_cfg.meta.run_nns      = False
_cfg.meta.run_coverage = True

_cfg.exp.path              = 'phd/c6/dov_reuse'
_cfg.exp.prefix_name       = ('dov_reuse',)
_cfg.exp.repetitions       = 25
_cfg.exp.seeds.exploration = factored.seeds
_cfg.job.steps             = 1000

_cfg.testscov.buffer_size   = 45/2.0
_cfg.testscov.ticks         = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, _cfg.job.steps+1, 25)]


# exps = [('dov_ball45_0.s', 'dov_ball45_0.s'),
#         ('dov_ball45_0.s', 'dov_cube45_0.s'),
#         ('dov_cube45_0.s', 'dov_cube45_0.s'),
#         ('dov_cube45_0.s', 'dov_ball45_0.s'),
#         ('dov_ball45_0.s', 'dov_ball45_4.s'), # misreuse
#         ('dov_ball45_4.s', 'dov_ball45_0.s'), # misreuse
#         ('dov_ball25_0.s', 'dov_ball25_0.s'),
#         ('dov_ball25_0.s', 'dov_cube25_0.s'),
#         ('dov_cube25_0.s', 'dov_cube25_0.s'),
#         ('dov_cube25_0.s', 'dov_ball25_0.s'),
#         ('dov_tube40_80_0.s', 'dov_ball45_0.s'),
#         ('dov_ball45_0.s', 'dov_tube40_80_0.s'),
#        ]


def findsize(s):
    return int(s.split('_')[1][-2:])

def findloc(s):
    return int(s.split('_')[2].split('.')[0])

def generate_expcfgs(exps,
                     src_ex_names=('random.goal_{}'.format(MB_STEPS), 'random.motor'),
                     reuse_algo=('sensor_uniform', 'random'),
                     expcfgs=None, rep=25, seeds=None, path='phd/c6/dov_reuse'):
    src_exps = set([e  for e, _ in exps] + [e  for _, e in exps])

    expcfgs_global = expcfgs
    if expcfgs_global is None:
        expcfgs_global = [[], []]
    expcfgs = [[], []]

    cfg = _cfg._deepcopy()
    cfg.exp.repetitions = rep
    cfg.exp.path        = path
    if seeds is not None:
        cfg.exp.seed.exploration = seeds

    for env_name in src_exps:
#         src_ex_names = ['random.goal_{}'.format(MB_STEPS)]
#         if random_motor:
# #        if findsize(env_name) == 45 and findloc(env_name) == 0:
#            ex_names.append('random.motor')

        for ex_name in src_ex_names:
            exp_cfg = cfg._deepcopy()

            exp_cfg.exploration.explorer._update(exs.catalog[ex_name], overwrite=False)
            exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

            exp_cfg.exp.key = ((exp_cfg.exp.prefix_name + (ex_name, env_name), cfg.exp.repetitions), ())
            exp_cfg.exp.explorer_name = ex_name
            exp_cfg.exp.env_name      = env_name
            expcfgs[0].append(exp_cfg)


    for src_cfg in expcfgs[0]:

        env_names = [e for d, e in exps if d == src_cfg.exp.env_name]

        for env_name in env_names:
            run = True

            algorithms = reuse_algo #['sensor_uniform']
#            if random_reuse: #findsize(env_name) in [45, 80]:
#               algorithms.append('random')

            # if (not (findsize(env_name) == 45 and findloc(src_cfg.exp.env_name) == 0 and findloc(env_name) == 0)
            #     and src_cfg.exp.explorer_name == 'random.motor'):
            #     run = False

            if run:
                for algorithm in algorithms:
                    ex_name, ex_cfg = exs.reuse_explorer(MB_STEPS, 0.5, 0.05, 20,  algorithm=algorithm)
                    exp_cfg = cfg._deepcopy()

                    exp_cfg.exploration.explorer = ex_cfg
                    exp_cfg.job.env._update(envs.catalog[env_name], overwrite=False)

                    exp_cfg.exp.deps = (src_cfg.exp.key[0],)
                    exp_cfg.exp.key = ((tuple(exp_cfg.exp.prefix_name) + (src_cfg.exp.explorer_name, src_cfg.exp.env_name, ex_name, env_name), cfg.exp.repetitions), exp_cfg.exp.deps)
                    exp_cfg.exp.explorer_name = ex_name
                    exp_cfg.exp.env_name      = env_name
                    expcfgs[1].append(exp_cfg)

    expcfgs_global[0] += expcfgs[0]
    expcfgs_global[1] += expcfgs[1]
    return expcfgs_global


def ball_cube_45(expcfgs=None):
    return generate_expcfgs([('dov_ball45_0.s', 'dov_ball45_0.s'),
                             ('dov_ball45_0.s', 'dov_cube45_0.s'),
                             ('dov_cube45_0.s', 'dov_cube45_0.s'),
                             ('dov_cube45_0.s', 'dov_ball45_0.s')],
                            expcfgs=expcfgs,
                            src_ex_names=('random_goal200',),
                            reuse_algo=('sensor_uniform', 'random'))

def ball_cube_45_random(expcfgs=None):
    return generate_expcfgs([('dov_ball45_0.s', 'dov_ball45_0.s'),
                             ('dov_cube45_0.s', 'dov_ball45_0.s')],
                            expcfgs=expcfgs,
                            src_ex_names=('random.motor'),
                            reuse_algo=('sensor_uniform', 'random'))

def misreuse(expcfgs=None):
    return generate_expcfgs([('dov_ball45_0.s', 'dov_ball45_4.s'),
                             ('dov_ball45_4.s', 'dov_ball45_0.s')],
                            expcfgs=expcfgs,
                            src_ex_names=('random_goal200',),
                            reuse_algo=('sensor_uniform', 'random'))

def cylinder_ball(expcfgs=None):
    return generate_expcfgs([('dov_tube40_80_0.s',    'dov_ball45_0.s'),
                             ('dov_tube40_80_0_rs.s', 'dov_ball45_0.s'),
                             #('dov_ball45_0.s',    'dov_tube40_80_0.s'),
                            ],
                            expcfgs=expcfgs,
                            src_ex_names=('random_goal200',),
                            reuse_algo=('sensor_uniform', 'random'))

def ball_cube_25(expcfgs=None):
    return generate_expcfgs([('dov_ball25_0.s', 'dov_ball25_0.s'),
                             ('dov_ball25_0.s', 'dov_cube25_0.s'),
                             ('dov_cube25_0.s', 'dov_cube25_0.s'),
                             ('dov_cube25_0.s', 'dov_ball25_0.s')],
                            expcfgs=expcfgs,
                            src_ex_names=('random_goal200',),
                            reuse_algo=('sensor_uniform',))


if __name__ == '__main__':
    expcfgs = [[], []]
    expcfgs = ball_cube_45(expcfgs)
    expcfgs = misreuse(expcfgs)
    expcfgs = cylinder_ball(expcfgs)
    expcfgs = ball_cube_25(expcfgs)

    explib.run([cfg for cfg_level in expcfgs for cfg in cfg_level])



