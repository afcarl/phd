import environments

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
            dataset['s_signals'].append(environments.tools.to_signal(s_vector, kin.s_channels))
            s_vectors.append(s_vector)

from clusterjobs import datafile
datafile.save_file(dataset, '../../testsets/testset_kinone')


if __name__ == '__main__':
    import graphs
    from bokeh import plotting
    plotting.output_file('../../../results/testset_kinone.html')

    graphs.bokeh_spread(kin.s_channels, s_vectors=s_vectors,
                        e_radius=1.5, e_alpha=0.75,
                        title='{} tests'.format(len(s_vectors)))
    plotting.grid().grid_line_color = 'white'

    plotting.show()
