import environments.envs
from environments import mprims

import envs_dov
#import envs_dmp2d
#import envs_vworlds


catalog = {}
#catalog.update(envs_dmp2d.catalog) # DMP2D
#catalog.update(envs_vworlds.catalog) # VWorlds
catalog.update(envs_dov.catalog) # Dovecot

def kin(dim=20, limit=150, lengths=None):
    kin_cfg = environments.envs.KinematicArm2D.defcfg._deepcopy()

    kin_cfg.dim = dim
    if lengths is None:
        kin_cfg.lengths = 1.0/kin_cfg.dim
    else:
        assert len(lengths) == dim
        kin_cfg.lengths = lengths
    kin_cfg.limits  = (-limit, limit)

    return kin_cfg



# KinArm2D
for dim in [2, 3, 5, 7, 8, 9, 10, 15, 20, 30, 40, 50, 60, 80, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900,1000, 2000]:
    for limit in [5, 10, 20, 45, 90, 120, 150, 180]:
        kin_cfg = environments.envs.KinematicArm2D.defcfg._deepcopy()
        kin_cfg.dim = dim
        kin_cfg.lengths = 1.0/kin_cfg.dim
        kin_cfg.limits  = (-limit, limit)
        catalog['kin{}_{}'.format(dim, limit)] = kin_cfg


for syn in [2, 3, 5, 10]:
    kin2ds_cfg          = environments.envs.KinArmSynergies2D.defcfg._deepcopy()
    kin2ds_cfg.dim      = 20
    kin2ds_cfg.lengths  = 1.0/kin2ds_cfg.dim
    kin2ds_cfg.limits   = (-150, 150)
    kin2ds_cfg.syn_span = syn
    kin2ds_cfg.syn_res  = syn

    catalog['kinsyn{}_{}'.format(kin2ds_cfg.dim, syn)] = kin2ds_cfg


catalog['vowels'] = environments.envs.VowelModel.defcfg._copy()
