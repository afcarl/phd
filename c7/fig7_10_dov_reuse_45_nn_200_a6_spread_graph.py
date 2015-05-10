# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import covgraph

import dotdot
import graphs

from fig7_10_dov_reuse_45_nn_200_a6_spread_cluster import expcfgs

#expcfgs_levels = generate_expcfgs([('dov_cube45_0.s', 'dov_ball45_0.s')])
covgraph.coverage_graphs(expcfgs, dest='c7_fig7_10_dov_reuse_covgraphs.html', n_graphs=10)
graphs.show()
