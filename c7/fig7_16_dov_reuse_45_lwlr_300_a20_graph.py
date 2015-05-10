# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

from reuse_perf_graphs import perf_graphs, load_results
from fig7_16_dov_reuse_45_lwlr_300_a20_cluster import expcfgs_levels

import dotdot
import graphs

# look at fig7_16_dov_reuse_45_lwlr_300_a20_cluster.py for full configuration details
sources, targets = load_results(expcfgs_levels)

graphs.output_file('c7_fig7_16_graph.html')
perf_graphs(sources, targets, mb_steps=300, y_maxs=(1000000, 400000))
graphs.show()
