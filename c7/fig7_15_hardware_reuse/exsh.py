# -*- coding: utf-8 -*-
""" The explorers's configuration for ICDL 2014

SourceExplorer
├── [100% [->300],  10% [->end]]
│   RandomMotorExplorer
│
├── [  0% [->300],  18% [->end]]
│   RandomGoalExplorer
│       learner.classname: learners.ModelLearner
│       learner.m_uniformize: True
│       learner.models.fwd: ES-LWLR
│       learner.models.inv: L-BFGS-B
│
└── [  0% [->300],  72% [->end]]
    MeshgridGoalExplorer
        res: 50
        learner.classname: learners.ModelLearner
        learner.m_uniformize: True
        learner.models.fwd: ES-LWLR
        learner.models.inv: L-BFGS-B

TargetExplorer
├── [ 50% [->300],   5% [->end]]
│   RandomMotorExplorer
│
├── [ 50% [->300],   5% [->end]]
│   ReuseExplorer
│       reuse.discount: 1.0
│       reuse.algorithm: sensor_uniform
│       reuse.res: 50
│
├── [  0% [->300],  18% [->end]]
│   RandomGoalExplorer
│       learner.classname: learners.ModelLearner
│       learner.m_uniformize: True
│       learner.models.fwd: ES-LWLR
│       learner.models.inv: L-BFGS-B
│
└── [  0% [->300],  72% [->end]]
    MeshgridGoalExplorer
        res: 50
        learner.classname: learners.ModelLearner
        learner.m_uniformize: True
        learner.models.fwd: ES-LWLR
        learner.models.inv: L-BFGS-B

"""

import collections
import explorers
import learners


catalog = collections.OrderedDict()

    # Source Explorer #

learn_cfg = learners.ModelLearner.defcfg._deepcopy()
learn_cfg.models.fwd = 'ES-LWLR'
learn_cfg.models.inv = 'L-BFGS-B'

res = 40

# Source

src_expl              = explorers.MetaExplorer.defcfg._deepcopy()
src_expl.eras         = (300, None)
src_expl.weights      = ((1.0, 0.0), (0.1, 0.9))

src_expl.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()

src_expl.ex_1         = explorers.RandomGoalExplorer.defcfg._deepcopy()
src_expl.ex_1.learner = learn_cfg

# src_expl.ex_2         = explorers.MeshgridGoalExplorer.defcfg._deepcopy()
# src_expl.ex_2.learner = learn_cfg
# src_expl.ex_2.res     = res

catalog['src_expl'] = src_expl


    # Reuse Explorer #


tgt_expl              = explorers.MetaExplorer.defcfg._deepcopy()
tgt_expl.eras         = (300, None)
tgt_expl.weights      = ((0.5, 0.5, 0.0), (0.05, 0.05, 0.9))

tgt_expl.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()

tgt_expl.ex_1                 = explorers.ReuseExplorer.defcfg._deepcopy()
tgt_expl.ex_1.reuse.algorithm = 'sensor_uniform'
tgt_expl.ex_1.reuse.res       = res
tgt_expl.ex_1.reuse.discount  = 1.0

tgt_expl.ex_2         = explorers.RandomGoalExplorer.defcfg._deepcopy()
tgt_expl.ex_2.learner = learn_cfg

# tgt_expl.ex_3         = explorers.MeshgridGoalExplorer.defcfg._deepcopy()
# tgt_expl.ex_3.learner = learn_cfg
# tgt_expl.ex_3.res     = res

catalog['tgt_expl'] = tgt_expl



if __name__ == "__main__":
    for name, cfg in catalog.items():
        print('\n## {}'.format(name))
        print(explorers.tools.explorer_ascii(cfg))
