# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import random

import explorers
import environments
from environments import tools

import dotdot
import exs
import envs
import factored
import graphs


DIM  = 20
RES  = 20
MB   = 50
N    = 5000

random.seed(0)


# making graphs
graphs.output_file('c5_fig5_2_reuse_picks.html')
timescale = [N]
mesh_colors = ['#E5E5E5']#[graphs.rgb2hex(graphs.rgba2rgb((255, 255, 255), (233,  78, 119, 0.5)))]

def pick(meshgrid, n=1):
    assert n == 1
    picks = []
    for b in meshgrid.nonempty_bins:
        c, s_signal, m_signal = b.draw()
        picks.append((m_signal, s_signal))
    return picks


# instanciating the environment, and the Meshgrid
env_name, env_cfg = envs.kin(dim=DIM, limit=150)
env = environments.Environment.create(env_cfg)

ex_cfg = exs.catalog['random.goal']._deepcopy()
ex_cfg.eras = (MB, None)
ex_cfg.m_channels = env.m_channels
ex_cfg.s_channels = env.s_channels
ex = explorers.Explorer.create(ex_cfg)

mesh = explorers.ExplorerMeshGrid({'res': RES}, env.s_channels, env.m_channels)

# running the exploration
explorations, s_vectors, s_goals = factored.run_exploration(env, ex, N, mesh=mesh)
mesh_picks = pick(mesh)

# Spread Graph
for t in [MB, 200, 400, N]:
    alpha = 1.0 if t != N else 0.5
    graphs.spread(mesh.s_channels, s_vectors=s_vectors[:t], grid=False,
                  e_radius=1.5, e_alpha=alpha, title='first arm - {} steps'.format(t))
    # graphs.hold(True)
    # if t == N:
    #     graphs.bokeh_spread(mesh.s_channels, s_vectors=[tools.to_vector(s, mesh.s_channels) for m, s in mesh_picks],
    #                         e_color='#DF6464', e_radius=2.0, e_alpha=1.0)

# Mesh Graph
graphs.mesh(mesh, s_vectors=s_vectors,
            mesh_colors=mesh_colors, mesh_timescale=timescale,
            e_radius=1.5, e_alpha=0.5, tile_ratio=1.0, title='first arm - selected effects')
graphs.hold(True)
graphs.bokeh_spread(mesh.s_channels, s_vectors=[tools.to_vector(s, mesh.s_channels) for m, s in mesh_picks],
                    e_color='#DF6464', e_radius=2.0, e_alpha=1.0, grid=False)

if __name__ == '__main__':
    graphs.show()

# Dataset
mesh_explorations = []
for m_signal, s_signal in mesh_picks:
    mesh_explorations.append(({'m_signal': m_signal}, {'s_signal': s_signal}))

dataset = {'m_channels': mesh.m_channels,
           's_channels': mesh.s_channels,
           'explorations': mesh_explorations}

full_dataset = {'m_channels': env.m_channels,
                's_channels': env.s_channels,
                'explorations': explorations}
