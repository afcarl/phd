# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import environments
from clusterjobs import datafile

import dotdot
import envs


kin_cfg = envs.catalog['kin20_150']
kin = environments.Environment.create(kin_cfg)

dataset = {'s_channels': kin.s_channels, 's_signals': []}
s_vectors = []

RES = 70

for i in range(RES):
    for j in range(RES):
        s_vector = [(k+0.5)/RES*(c.bounds[1]-c.bounds[0])+ c.bounds[0] for k, c in zip([i, j], kin.s_channels)]
        if s_vector[0]**2 + s_vector[1]**2 <= 1.0:
            s_signal = environments.tools.to_signal(s_vector, kin.s_channels)
            dataset['s_signals'].append(s_signal)
            s_vectors.append(s_vector)

datafile.save_file(dataset, '../../testsets/testset_kinone')

if __name__ == '__main__':
    import graphs
    graphs.output_file('c3_fig3_1_kin_testset.html')
    graphs.spread(kin.s_channels, s_vectors=s_vectors,
                  e_radius=1.5, e_alpha=0.75,
                  title='{} tests'.format(len(s_vectors)))
    graphs.grid().grid_line_color = 'white'
    graphs.show()
