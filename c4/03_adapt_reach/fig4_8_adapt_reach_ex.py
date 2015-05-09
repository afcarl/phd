# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import explorers
import learners

# Explorer Config
ex1_cfg = explorers.AdaptExplorer.defcfg._deepcopy()
ex1_cfg.div_algorithm = 'hyperball'
ex1_cfg.threshold     = 0.05
ex1_cfg.window        = 50
ex1_cfg.random_ratio  = 0.1
ex1_cfg.head_start    = 1
ex1_cfg.fallback      = 0

ex1_cfg.ex_0         = explorers.MeshgridGoalExplorer.defcfg._deepcopy()
ex1_cfg.ex_0.learner = learners.DisturbLearner.defcfg._deepcopy()
ex1_cfg.ex_0.learner.m_disturb = 0.05
ex1_cfg.ex_0.res     = 40

ex1_cfg.ex_1         = explorers.UnreachGoalExplorer.defcfg._deepcopy()
ex1_cfg.ex_1.learner = learners.DisturbLearner.defcfg._deepcopy()
ex1_cfg.ex_1.learner.m_disturb = 0.05
ex1_cfg.ex_1.res     = 40

ex_cfg              = explorers.MetaExplorer.defcfg._deepcopy()
ex_cfg.eras         = (10, None)
ex_cfg.weights      = ((1.0, 0.0), (0.0, 1.0))

ex_cfg.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()
ex_cfg.ex_1         = ex1_cfg

grid_cfg = ex_cfg._deepcopy()
grid_cfg.ex_1._pop('threshold')
grid_cfg.ex_1.div_algorithm = 'grid'
grid_cfg.ex_1.gamma = 0.5
grid_cfg.ex_1.res   = 40

