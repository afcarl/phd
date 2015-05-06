# -*- coding: utf-8 -*-
import collections
import explorers
import learners


catalog = {}



    # Learners #

learn_cfg = learners.DisturbLearner.defcfg._deepcopy()
learn_cfg.m_disturb = 0.05

learn2_cfg = learners.DisturbTwoStepLearner.defcfg._deepcopy()
learn2_cfg.m_disturb = 0.05

lwlr_cfg = learners.ModelLearner.defcfg._copy(deep=True)
lwlr_cfg.models.fwd = 'ES-LWLR'
lwlr_cfg.models.inv = 'L-BFGS-B'

plwlr_cfg = learners.PredictDisturbLearner.defcfg._copy(deep=True)
plwlr_cfg.attempts    = 10
plwlr_cfg.m_disturb   = 0.05
plwlr_cfg.fwd         = lwlr_cfg


    # Explorers #

# Random Motor

rm_expl = explorers.RandomMotorExplorer.defcfg._deepcopy()
catalog['random.motor'] = rm_expl


# Random Goal

rg_expl              = explorers.MetaExplorer.defcfg._deepcopy()
rg_expl.eras         = (10, None)
rg_expl.weights      = ((1.0, 0.0), (0.0, 1.0))

rg_expl.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()

rg_expl.ex_1         = explorers.RandomGoalExplorer.defcfg._deepcopy()
rg_expl.ex_1.learner = learn_cfg

catalog['random.goal'] = rg_expl

for d in [0.001, 0.0025, 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0]:
    rg_ex = rg_expl._deepcopy()
    rg_ex.ex_1.learner.m_disturb = d
    catalog['random.goal_d{}'.format(d)] = rg_ex


rg2_expl = rg_expl._deepcopy()
rg2_expl.ex_1.learner = learn2_cfg

catalog['random.goal2'] = rg2_expl


for mb in [1, 10, 20, 25, 50, 100, 200, 250, 300, 500, 1000, 4000, 4500, 4750, 4900, 24000, 24500, 49000]:
    rg_expl_mb = rg_expl._deepcopy()
    rg_expl_mb.eras = (mb, None)
    catalog['random.goal_{}'.format(mb)] = rg_expl_mb



# Meshgrid/Random Goal

res = 20

for i in range(0, 101, 5):
    mesh_expl              = explorers.MetaExplorer.defcfg._deepcopy()
    mesh_expl.eras         = (10, None)
    mesh_expl.weights      = ((1.0, 0.0, 0.0), (0.0, 1.0-i/100.0, i/100.0))

    mesh_expl.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()

    mesh_expl.ex_1         = explorers.MeshgridGoalExplorer.defcfg._deepcopy()
    mesh_expl.ex_1.learner = learn_cfg
    mesh_expl.ex_1.res     = res

    mesh_expl.ex_2         = explorers.UnreachGoalExplorer.defcfg._deepcopy()
    mesh_expl.ex_2.learner = learn_cfg
    mesh_expl.ex_2.res     = res

    catalog['unreach_{}'.format(i)] = mesh_expl

for d in [0.5, 2, 10]:
    rg_bound = explorers.RestrictGoalExplorer.defcfg._deepcopy()
    rg_bound.manual_s_bounds = {'x': (-d, d), 'y': (-d, d)}
    rg_bound.explorer = rg_expl._deepcopy()
    catalog['distrib{}'.format(d)] = rg_bound

rg_bound = explorers.RestrictGoalExplorer.defcfg._deepcopy()
rg_bound.manual_s_bounds = {'x': (-0.75, -0.5), 'y': (0.5, 0.75)}
rg_bound.explorer = rg_expl._deepcopy()
catalog['distrib_corner'] = rg_bound

for n in [1, 3, 5, 10, 20, 50, 100]:
    motor_expl = explorers.MotorDisturbExplorer.defcfg._deepcopy()
    motor_expl.res = 20
    motor_expl.m_disturb = 0.05
    motor_expl.n_perturbations = n
    catalog['disturb.motor{}'.format(n)] = motor_expl


def frontier_ex(mb, m_disturb, res):
    frontier_cfg              = explorers.MetaExplorer.defcfg._deepcopy()
    frontier_cfg.eras         = (mb, None)
    frontier_cfg.weights      = ((1.0, 0.0), (0.0, 1.0))

    frontier_cfg.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()

    frontier_cfg.ex_1         = explorers.FrontierGoalExplorer.defcfg._deepcopy()
    frontier_cfg.ex_1.learner = learn_cfg
    frontier_cfg.ex_1.learner.m_disturb = m_disturb
    frontier_cfg.ex_1.res     = res

    return 'frontier{}_{}_{}'.format(mb, m_disturb, res), frontier_cfg

# Reuse Goals

def reuse_explorer(mb, reuse_usage, m_disturb, res, algorithm='sensor_uniform'):
    assert 0 <= reuse_usage <= 1

    reuse_ex          = explorers.MetaExplorer.defcfg._deepcopy()
    reuse_ex.eras     = (mb, None)
    reuse_ex.weights  = ((reuse_usage, 1-reuse_usage, 0.0), (0.0, 0.0, 1.0))

    reuse_ex.ex_0     = explorers.ReuseExplorer.defcfg._deepcopy()
    reuse_ex.ex_0.reuse.res = res
    reuse_ex.ex_0.reuse.algorithm = algorithm

    reuse_ex.ex_1     = explorers.RandomMotorExplorer.defcfg._deepcopy()

    reuse_ex.ex_2                   = explorers.RandomGoalExplorer.defcfg._deepcopy()
    reuse_ex.ex_2.res               = res
    reuse_ex.ex_2.learner           = learn_cfg
    reuse_ex.ex_2.learner.m_disturb = m_disturb

    algsrc = ''
    if algorithm != 'sensor_uniform':
        algsrc = '.' + algorithm
    return 'reuse{}_{}_{}_{}_{}'.format(algsrc, mb, reuse_usage, m_disturb, res), reuse_ex


if __name__ == "__main__":
    for name, cfg in catalog.items():
        print('\n## {}'.format(name))
        print(explorers.tools.explorer_ascii(cfg))
