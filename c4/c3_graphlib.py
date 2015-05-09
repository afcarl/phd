from __future__ import division

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../..')))


import graphs


def adapt_graphs(ex_cfg, explorations, s_vectors, weight_history, mesh=None, title='no title'):
    s_channels = ex_cfg.s_channels

    tally_dict = {}
    for exploration, feedback in explorations:
        tally_dict.setdefault(exploration['from'], 0)
        tally_dict[exploration['from']] += 1
    print(tally_dict)

    if ex_cfg.div_algorithm == 'hyperball':
        graphs.coverage(s_channels, ex_cfg.threshold, s_vectors=s_vectors, title=title)
    else:
        assert ex_cfg.div_algorithm == 'grid'
        if mesh is not None:
            graphs.mesh(mesh, title=title)
    graphs.hold(True)
    graphs.spread(s_channels, s_vectors=s_vectors, e_radius=1.25, e_alpha=0.75)


    # interest measure
    colors = [graphs.BLUE, graphs.PINK]
    weight_lists = zip(*weight_history['data'])
    for i, weights in enumerate(weight_lists):
        graphs.perf_std(range(len(weights)), weights, [0.0 for _ in weights],
                        legend=weight_history['ex_names'][i], color=colors[i], alpha=0.5,
                        plot_width=1000, plot_height=300, title='diversity: {}'.format(title))
        graphs.hold(True)
    graphs.hold(False)

    # # usage with sliding window
    window = 100.0

    uuid_history = tuple(e[0]['uuid'] for e in explorations)
    for i, weights in enumerate(weight_lists):
        ex_uuid = weight_history['ex_uuids'][i]
        ex_name = weight_history['ex_names'][i]

        usage = [t_usage(window, t, ex_uuid, uuid_history) for t in range(len(uuid_history))]
        graphs.perf_std(range(len(usage)), usage, [0.0 for _ in usage], color=colors[i], alpha=0.5,
                          plot_width=1000, plot_height=300, title='usage: {}'.format(title), y_range=(0.0, 1.0))
        graphs.hold(True)

    graphs.hold(False)
    # print('{} {:.3f}'.format(env_name, np.average(errors)))
    return tally_dict

def t_usage(window, t, uuid, uuid_history):
    t_min = max(0, t-int(window/2))
    t_max = min(len(uuid_history), t+int(window/2))
    return sum(h_i == uuid for h_i in uuid_history[t_min:t_max])/(t_max-t_min)

def usage_graph(ex_cfg, explorations, weight_history, title='no title'):
    colors = [graphs.BLUE, graphs.PINK]
    window = 100.0

    uuid_history = tuple(e[0]['uuid'] for e in explorations)
    for i, weights in enumerate(weight_lists):
        ex_uuid = weight_history['ex_uuids'][i]
        ex_name = weight_history['ex_names'][i]

        usage = [t_usage(window, t, ex_uuid, uuid_history) for t in range(len(uuid_history))]
        graphs.perf_std(range(len(usage)), usage, [0.0 for _ in usage], color=colors[i], alpha=0.5,
                          plot_width=1000, plot_height=300, title='usage: {}'.format(title), y_range=(0.0, 1.0))
        graphs.hold(True)

    graphs.hold(False)
