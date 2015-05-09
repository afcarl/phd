# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import explorers

import dotdot
import exs

ex_cfg = explorers.AdaptExplorer.defcfg._deepcopy()
ex_cfg.div_algorithm = 'hyperball'
ex_cfg.threshold = 0.02
ex_cfg.window = 50
ex_cfg.random_ratio = 0.1
ex_cfg.head_start = 1
ex_cfg.fallback = 0
ex_cfg.ex_0 = exs.catalog['random.goal'].ex_0._deepcopy()
ex_cfg.ex_1 = exs.catalog['random.goal'].ex_1._deepcopy()

grid_cfg = ex_cfg._deepcopy()
grid_cfg._pop('threshold')
grid_cfg.div_algorithm = 'grid'
grid_cfg.gamma         = 0.5
grid_cfg.res           = 40
