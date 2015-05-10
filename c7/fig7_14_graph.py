# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

from reuse_perf_graphs import perf_graphs, load_results
from fig7_10_14_dov_reuse_2545_nn_200_a6 import cylinder_ball

import dotdot
import graphs

# look at fig7_10_14_dov_reuse_2545_nn_200_a6.py for full configuration details
exp_cfgs = cylinder_ball()
sources, targets = load_results(exp_cfgs)

graphs.output_file('c7_fig7_14_graph.html')
perf_graphs(sources, targets)
graphs.show()
