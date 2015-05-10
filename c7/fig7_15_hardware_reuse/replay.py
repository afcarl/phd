from __future__ import division

import os

import environments
import gfx

from explib.jobs import jobfactory
from explib.graphs import hub

import dotdot
import envs

env_name = 'scaff_b45_3_b45_light.s' #'scaffold_ball45_0.s'
env_name = 'ball_45_0.s'

def dovecot_replay(exp_cfg, rep, collision_only=True, headless=False):

    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

    data_hub = hub.DataHub(batch, folder='/Users/fabien/research/data.hard/', verbose=True)
    job_data = data_hub.data()
    job_data = job_data[rep]
    assert job_data.job.cfg.job.rep == rep

    job_cfg = job_data.jobcfg._deepcopy()
    job_cfg.job._freeze(False)

    env_cfg = job_cfg.job.env
    env_cfg = envs.catalog[env_name]
    if headless:
        env_cfg.execute.simu.ppf = 200
        env_cfg.execute.simu.headless = True
    else:
        env_cfg.execute.simu.ppf = 1
        env_cfg.execute.simu.headless = False

    env = environments.Environment.create(env_cfg)

    raw_input()
    assert job_data.observations is not None, "motor signals (observations) could not be loaded (datafiles probably missing)."
    print('obs from file: {}{}{}'.format(gfx.green, job_cfg.exploration.hardware.datafile, gfx.end))
    for step, (m_signal, s_signal) in enumerate(job_data.observations):

        if not collision_only or s_signal['push_saliency'] != 0:
#            if s_signal['x'] > 100.0 and s_signal['y'] > 100.0:
            #if step in [896, 786, 648, 414]:
                #assert s_signal['push_saliency'] > 999
            print('{:04d} {}{}{} [recorded]'.format(step, gfx.cyan, s_signal, gfx.end))
            feedback = env.execute(m_signal)
            print('     {}'.format(feedback['s_signal']))
        raw_input()


if __name__ == '__main__':
    from tgt_exp import expcfgs_levels
    dovecot_replay(expcfgs_levels[1][0], 0)
