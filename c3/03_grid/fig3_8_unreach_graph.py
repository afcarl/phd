import os

from bokeh import plotting

from explib.graphs import hub
from explib.jobs import jobfactory

import dotdot
import graphs
from fig3_8_unreach_cluster import expcfgs_levels


exp_cfgs = expcfgs_levels[0]

ticks = [2000, 10000]
ratios_  = range(0, 101, 5)
ratios, avgs, stds = {tick: [] for tick in ticks}, {tick: [] for tick in ticks}, {tick: [] for tick in ticks}
y_max = 0.0

cwd = os.getcwd()

for i, exp_cfg in enumerate(exp_cfgs):
    batch = jobfactory.make_jobgroup([exp_cfg])
    os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

    results_hub = hub.ResultsHub(batch, kind='nn')
    src_data = results_hub.data()
    assert len(src_data) == 1

    for tick in ticks:

        try:
            index = src_data[0]['ticks'].index(tick)
            ratios[tick].append(ratios_[i])
            avgs[tick].append(src_data[0]['avg'][index])
            stds[tick].append(src_data[0]['std'][index])
            y_max = max(y_max, max(avgs[tick]) + max(stds[tick]))
        except ValueError:
            pass

os.chdir(cwd)


if __name__ == "__main__":
    print('  '.join('{:6.3f}|{:6.3f}'.format(a,s) for a, s in zip(avgs, stds)))
    plotting.output_file('../../../results/c3_fig3_8_unreach_perf.html')
    colors = ['#2577B2', '#E84A5F']

    for color, tick in zip(colors, [2000, 10000]):
        graphs.bokeh_std_discrete(ratios[tick], avgs[tick], stds[tick],
                                  std_width=0.25, color=color, alpha=0.75,
                                  y_range=[0.0, y_max + 0.01], #y_range=[y_min-0.1, y_max+0.1],
                                  plot_width=1000, plot_height=400, title='t={}'.format(tick))
        plotting.hold(True)

    plotting.show()

