# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

from reuse_perf_graphs import perf_graphs, load_results
from fig7_10_14_dov_reuse_2545_nn_200_a6 import ball_cube_45_random

import dotdot
import graphs

# look at fig7_10_14_dov_reuse_2545_nn_200_a6.py for full configuration details
exp_cfgs = ball_cube_45_random()
sources, targets = load_results(exp_cfgs)

graphs.output_file('c7_fig7_13_graph.html')
perf_graphs(sources, targets)
graphs.show()
