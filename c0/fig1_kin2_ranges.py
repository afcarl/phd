from bokeh import plotting

import environments

import dotdot
import envs
import graphs


# instanciating the environment
env_cfg = envs.catalog['kin2_150']._deepcopy()
env = environments.Environment.create(env_cfg)

# making graphs
plotting.output_file('../../results/c0_fig1_kin2_ranges.html')
for a in range(-150, 150, 10):
    graphs.bokeh_kin(env, [{'j0': 0, 'j1': a}],
                     color='#333333', alpha=a*0.0005+0.3,
                     swap_xy=True, title='joint ranges')
    plotting.hold(True)

for a in range(0, 151, 15):
    graphs.bokeh_kin(env, [{'j0': a, 'j1': 150}], color='#666666',
                     alpha=0.5)
    plotting.hold(True)
plotting.show()
