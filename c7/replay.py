from __future__ import division

import os

import environments
import gfx

from explib.jobs import jobfactory
from explib.graphs import hub

import dotdot
import envs
import obslib

#env_name = 'scaff_b45_3_b45_light.s' #'scaffold_ball45_0.s'
#env_name = 'noobj.s'
#env_name = 'ball45_0_a20.s'
env_name = 'ball25_0.s'
#env_name = 'tube40_80_0.s'
#env_name = 'cube45_0.s'

#env_name = 'noobj.s'

def dovecot_replay(exp_cfg, rep, collision_only=True, headless=False):

    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

    data_hub = hub.DataHub(batch, folder='/Users/fabien/research/data.sim/', verbose=True)
    job_data = data_hub.data()
    job_data = job_data[rep]
    assert job_data.job.cfg.job.rep == rep

    job_cfg = job_data.jobcfg._deepcopy()
    job_cfg.job._freeze(False)

    env_cfg = job_cfg.job.env
    env_cfg = envs.catalog[env_name]
    env_cfg.execute.prefilter = False
    env_cfg.execute.simu.calibr_check = False
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

    for step, (expl, fback) in enumerate(job_data.explorations):
        s_vector = environments.tools.to_vector(fback['s_signal'], job_data.s_channels)
        print('{}:{}: {}'.format(step, s_vector[-1], expl['from']))

    step = -1
    while True:
        print('choose a step:')
        inp = raw_input()
        if inp == '':
            step += 1
        elif inp == '=':
            step += 0 # no change
        else:
            step = int(inp)

        expl, fback = job_data.explorations[step]
        m_signal = expl['m_signal']
        s_signal = fback['s_signal']

    # for step, (expl, fback) in enumerate(job_data.explorations):
    #     m_signal = expl['m_signal']
    #     s_signal = fback['s_signal']

        # print(m_signal)
        # m_signal = environments.tools.random_signal(job_data.m_channels)
        # print(m_signal)



        print('{:04d} {}'.format(step, expl['from']))

        # if step in [50, 49, 7, 19, 15]:
        # if (expl['from'] == 'goal.babbling'):
        #     if s_signal['push_saliency'] == 0:
#            if (not collision_only or s_signal['push_saliency'] == 0):

    #            if s_signal['x'] > 100.0 and s_signal['y'] > 100.0:
                #if step in [896, 786, 648, 414]:
                    #assert s_signal['push_saliency'] > 999
            # for _ in range(5):
        print('{:04d} {}{}{} [recorded]'.format(step, gfx.cyan, s_signal, gfx.end))
        feedback = env.execute(m_signal)
        print('     {}'.format(feedback['s_signal']))
            # raw_input()
            # m_signal = obslib.add_noise(m_signal, job_data.m_channels, 0.05)
            # feedback = env.execute(m_signal)
            # print('     {}'.format(feedback['s_signal']))
            # raw_input()


if __name__ == '__main__':
    from dov_sources import expcfgs_levels
    dovecot_replay(expcfgs_levels[0][0], 0, collision_only=True, headless=False)
