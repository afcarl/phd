# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import explib

import fig7_10_14_dov_reuse_2545_nn_200_a6

# generate_expcfgs([('dov_cube45_0.s', 'dov_ball45_0.s')], random_motor=False, random_reuse=False,
#                  expcfgs=None, rep=1, seeds=[0], path='phd/c6/dov_reuse_zero'):

#fig7_10_14_dov_reuse_2545_nn_200_a6._cfg.exp.repetitions = 1
fig7_10_14_dov_reuse_2545_nn_200_a6._cfg.exp.path        = 'phd/c7/dov_reuse_zero'
expcfgs = fig7_10_14_dov_reuse_2545_nn_200_a6.generate_expcfgs([('dov_cube45_0.s', 'dov_ball45_0.s')],
                                                               src_ex_names=('random_goal200',),
                                                               reuse_algo=('sensor_uniform'), rep=1)


for i, level in enumerate(expcfgs):
    for exp_cfg in level:
        exp_cfg.exp.seeds.exploration = [i]

if __name__ == '__main__':
    explib.run([cfg for cfg_level in expcfgs for cfg in cfg_level])

