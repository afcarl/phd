import os, sys


from environments import tools
from explib.graphs import hub
from explib.jobs import jobfactory
from explib.jobs.execute import load_module

import dotdot
import graphs


def coverage_graphs(expcfgs_levels, dest='tmp.html', n_graphs=3):
    cwd = os.getcwd()
    graphs.output_file(dest)

    red = '#DF6464'

    for level in expcfgs_levels:
        for i, exp_cfg in enumerate(level):
            n = 0
            batch = jobfactory.make_jobgroup([exp_cfg])
            os.chdir(os.path.expanduser(exp_cfg.meta.rootpath))

            data_hub = hub.DataHub(batch, sensory_only=True)
            datas = data_hub.data()

            for j, data in enumerate(datas):
                if n_graphs is None or n < n_graphs:
                    for N in [200, 1000]:
                        print(exp_cfg.exploration.explorer)
                        n_reuse = exp_cfg.exploration.explorer.eras[0]
                        s_vectors = [tools.to_vector(s_signal, data.s_channels) for s_signal in data.s_signals][:N]

                        graphs.coverage(data.s_channels, exp_cfg.testscov.buffer_size, s_vectors=s_vectors, swap_xy=False,
                                        title_text_font_size= '6pt',
                                        title='{} {}'.format(exp_cfg.exp.key, j))
                        graphs.hold(True)
                        graphs.spread(data.s_channels, s_vectors=s_vectors[n_reuse:], swap_xy=False, e_radius=2.0)
                        graphs.hold(True)
                        graphs.spread(data.s_channels, s_vectors=s_vectors[:n_reuse], swap_xy=False, e_radius=2.0, e_color=red)
                        n += 1

    os.chdir(cwd)
