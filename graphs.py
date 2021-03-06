from __future__ import division, print_function

import os
import bisect
import struct
import numbers
import math
import random

import numpy as np
from bokeh import plotting

try:
    import shapely
    import shapely.ops
    import shapely.geometry
except ImportError:
    pass

from environments import tools

import factored


    ## color

BLUE  = '#2577B2' # light blue
PINK  = '#E84A5F'
GREEN = '#5AB953'

MB_COLOR = BLUE
GB_COLOR = PINK

NOREUSE_COLOR   = BLUE
REUSE_COLOR     = PINK
RANDREUSE_COLOR = '#408000' # green

E_COLOR = '#2779B3' # blue
G_COLOR = '#FF030D' # red


white   = (255, 255, 255)

def rgb2hex(rgb):
    return '#{0:02x}{1:02x}{2:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hex2rgb(hexstr):
    return struct.unpack('BBB', hexstr[1:].decode('hex'))

def rgba2rgb(rgb, rgba):
    r,g,b,a = rgba;
    return ((1-a)*rgb[0] + a * r,
            (1-a)*rgb[1] + a * g,
            (1-a)*rgb[2] + a * b)

C_COLOR   = rgb2hex((21, 152, 71))
#C_COLOR_H = rgb2hex(rgba2rgb(white, (21, 152, 71, 0.5)))
C_COLOR_H = rgb2hex((200, 200, 200))

def hexa(hex, alpha):
    rgb = hex2rgb(hex)
    return rgb2hex(rgba2rgb((255, 255, 255), rgb+(alpha,)))

def colorscale(timescale, rgb, alpha_step=0.15):
    color_n = len(timescale)
    colors = [rgba2rgb((255, 255, 255), rgb+(1.0-alpha_step*i,)) for i in range(color_n)]
    return [rgb2hex(c) for c in colors]

def ranges(s_channels, x_range=None, y_range=None):
    if x_range is None:
        x_range = s_channels[0].bounds
    if y_range is None:
        y_range = s_channels[1].bounds
    epsilon = 0.0000001 # HACK
    x_range = (x_range[0] - epsilon, x_range[1] + epsilon)
    y_range = (y_range[0] - epsilon, y_range[1] + epsilon)
    return x_range, y_range


    ## bokeh wrapping

results_dir = os.path.abspath(os.path.join(__file__, '../../results'))
def output_file(filepath):
    return plotting.output_file(os.path.join(results_dir, filepath))

def hold(flag):
    return plotting.hold(flag)

def show():
    return plotting.show()

def grid():
    return plotting.grid()


    ## displaying kinematic 2D arm postures

def posture_vectors(env, m_vectors, **kwargs):
    m_signals = [tools.to_signal(m_vector, env.m_channels) for m_vector in m_vectors]
    return posture_signals(env, m_signals, **kwargs)

def posture_extrema(env, explorations, thetas=tuple(i*math.pi/4 for i in range(8)), **kwargs):
    s_vectors = [tools.to_vector(e[1]['s_signal'], env.s_channels) for e in explorations]
    idxs = factored.spread_extrema(s_vectors, dirs=thetas)
    m_signals = [explorations[idx][0]['m_signal'] for idx in idxs]
    posture_signals(env, m_signals, **kwargs)

def posture_idxs(env, explorations, idxs=None, **kwargs):
    if idxs is None:
        idxs=[int(len(explorations)*i/5.0) for i in range(5)]
    posture_signals(env, [explorations[i][0]['m_signal'] for i in idxs], **kwargs)

def posture_random(env, explorations, n=5, **kwargs):
    m_display = choose_m_vectors(env.m_channels, explorations, n=n)
    posture_vectors(env, m_display, **kwargs)

def choose_m_vectors(m_channels, explorations, n=5):
    """FIXME: no replacements"""
    m_vectors = []
    for _ in range(n):
        explo = random.choice(explorations)
        m_vector = tools.to_vector(explo[0]['m_signal'], m_channels)
        m_vectors.append(m_vector)

    return m_vectors

#'#91C46C'
def posture_signals(kin_env, m_signals, title='posture graphs',
                    color='#666666', alpha=1.0, radius_factor=1.0,
                    swap_xy=True, x_range=[-1.0, 1.0], y_range=[-1.0, 1.0], **kwargs):

    for m_signal in m_signals:
        m_vector = kin_env.flatten_synergies(m_signal)
        s_signal = kin_env._multiarm.forward_kin(m_vector)

        xs, ys = [0.0], [0.0]
        for i in range(kin_env.cfg.dim):
            xs.append(s_signal['x{}'.format(i+1)])
            ys.append(s_signal['y{}'.format(i+1)])

        if isinstance(kin_env.cfg.lengths, numbers.Real):
            total_length = kin_env.cfg.lengths*kin_env.cfg.dim
        else:
            total_length = sum(kin_env.cfg.lengths)
        total_length += 0.0

        kwargs.update({'x_range'     : x_range,
                       'y_range'     : y_range,
                       'line_color'  : color,
                       'line_alpha'  : alpha,
                       'fill_color'  : color,
                       'fill_alpha'  : alpha,
                       'title'       : title
                      })

        if swap_xy:
            xs, ys = ys, xs

        plotting.line(xs, ys, line_width=2.0*radius_factor, **kwargs)
        plotting.hold(True)
        plotting.grid().grid_line_color = None
        plotting.ygrid().grid_line_color = None
        plotting_axis()

        plotting.circle(xs[  : 1], ys[  : 1], radius=radius_factor*0.015, **kwargs)
        plotting.circle(xs[ 1:-1], ys[ 1:-1], radius=radius_factor*0.008, **kwargs)
        plotting.circle(xs[-1:  ], ys[-1:  ], radius=radius_factor*0.01, color='red', alpha=alpha)
    plotting.hold(False)


    ## wrapping plots

def line(x_range, avg, std, color='#E84A5F', dashes=(4, 2), alpha=1.0):
    plotting.line(x_range, [avg, avg], line_color=color, line_dash=list(dashes), line_alpha=alpha)
    plotting.hold(True)
    plotting.rect([(x_range[0]+x_range[1])/2.0], [avg], [x_range[1]-x_range[0]], [2*std],
                  fill_color=color, line_color=None, fill_alpha=0.1*alpha)
    plotting.hold(False)

def spread(s_channels, s_vectors=(), s_goals=(),
           title='no title', swap_xy=True, x_range=None, y_range=None,
           e_radius=1.0, e_color=E_COLOR, e_alpha=0.75,
           g_radius=1.0, g_color=G_COLOR, g_alpha=0.75,
           grid=True, radius_units='screen', font_size='11pt', **kwargs):

    x_range, y_range = ranges(s_channels, x_range=x_range, y_range=y_range)

    # effects
    try:
        xv, yv = zip(*(s[:2] for s in s_vectors))
    except ValueError:
        xv, yv = [], []
    if swap_xy:
        x_range, y_range = y_range, x_range
        xv, yv = yv, xv
    plotting.scatter(xv, yv, title=title,
                     x_range=x_range, y_range=y_range,
                     fill_color=e_color, fill_alpha=e_alpha, line_color=None,
                     radius=e_radius, radius_units=radius_units, **kwargs)
#                     title_text_font_size=font_size, **kwargs)
    plotting.hold(True)

    # goals
    try:
        xg, yg = zip(*s_goals)
    except ValueError:
        xg, yg = [], []
    if swap_xy:
        xg, yg = yg, xg
    plotting.scatter(xg, yg, radius=g_radius, radius_units="screen", fill_color=g_color, fill_alpha=g_alpha, line_color=None)

    plotting_axis()
    if not grid:
        plotting.grid().grid_line_color = None
    plotting.hold(False)

bokeh_spread = spread

def coverage(s_channels, threshold, s_vectors=(),
                   title='no title', swap_xy=True, x_range=None, y_range=None,
                   color=C_COLOR, c_alpha=1.0, alpha=0.5, **kwargs):

    x_range, y_range = ranges(s_channels, x_range=x_range, y_range=y_range)
    try:
        xv, yv = zip(*(s[:2] for s in s_vectors))
    except ValueError:
        xv, yv = [], []
    if swap_xy:
        x_range, y_range = y_range, x_range
        xv, yv = yv, xv

    plotting.circle(xv, yv, radius=threshold, x_range=x_range, y_range=y_range,
                   fill_color=hexa(color, 0.35), fill_alpha=c_alpha, line_color=None,
                   title=title, **kwargs)
    plotting.hold(True)


    union = shapely.ops.unary_union([shapely.geometry.Point(*sv_i).buffer(threshold)
                                     for sv_i in s_vectors])
    boundary = union.boundary
    if isinstance(boundary, shapely.geometry.LineString):
        boundary = [boundary]

    for b in boundary:
        x, y = b.xy
        x, y = list(x), list(y)
        if swap_xy:
            x, y = y, x
        plotting.patch(x, y, fill_color=None, line_color=hexa(color, 0.75))
        plotting.hold(True)

    plotting_axis()
    plotting.hold(False)

bokeh_coverage = coverage

def bokeh_nn(s_channels, testset, errors,
             title='no title', swap_xy=True, x_range=None, y_range=None,
             radius=3.0, alpha=0.75):

    x_range, y_range = ranges(s_channels, x_range=x_range, y_range=y_range)
    xv, yv = zip(*testset)
    if swap_xy:
        x_range, y_range = y_range, x_range
        xv, yv = yv, xv

    scale = [0, max(errors)]
    colorbar = ColorBar(scale, ['#0000FF', '#FF0000'], continuous=True)
    colors = [colorbar.color(e) for e in errors]

    plotting.scatter(xv, yv, title=title,
                     x_range=x_range, y_range=y_range,
                     fill_color=colors, fill_alpha=alpha, line_color=None,
                     radius=radius, radius_units="screen")
    plotting.hold(True)
    plotting.grid().grid_line_color='white'
    plotting.hold(False)

def mesh(meshgrid, s_vectors=(), s_goals=(),
         mesh_timescale=(1000000,), mesh_colors=(C_COLOR_H,), title='no title',
         e_radius=1.0, e_color=E_COLOR, e_alpha=0.75,
         g_radius=1.0, g_color=G_COLOR, g_alpha=0.75, swap_xy=True, tile_ratio=0.97,
         x_range=None, y_range=None):

    x_range, y_range = ranges(meshgrid.s_channels, x_range=x_range, y_range=y_range)
    xm = zip(*[b.bounds[0] for b in meshgrid.nonempty_bins])
    ym = zip(*[b.bounds[1] for b in meshgrid.nonempty_bins])
    if swap_xy:
        x_range, y_range = y_range, x_range
        xm, ym = ym, xm

    color = []
    for b in meshgrid.nonempty_bins:
        t = b.elements[0][0]
        color.append(mesh_colors[bisect.bisect_left(mesh_timescale, t)])

    plotting.rect((np.array(xm[1])+np.array(xm[0]))/2         , (np.array(ym[1])+np.array(ym[0]))/2,
                  (np.array(xm[1])-np.array(xm[0]))*tile_ratio, (np.array(ym[1])-np.array(ym[0]))*tile_ratio,
                  x_range=x_range, y_range=y_range,
                  fill_color=color, fill_alpha=0.5,
                  line_color='#444444', line_alpha=0.0, title=title)
    plotting.hold(True)
    plotting.grid().grid_line_color='white'

    spread(meshgrid.s_channels, s_vectors=s_vectors, s_goals=s_goals, swap_xy=swap_xy,
           e_radius=e_radius, e_color=e_color, e_alpha=e_alpha,
           g_radius=g_radius, g_color=g_color, g_alpha=g_alpha)
    plotting.hold(False)


def bokeh_highlights(s_vectors, n=1, color='#DF4949', swap_xy=True, radius=2.5, alpha=0.5):
    """n is the number of effect per cell to pick"""
    xv, yv = zip(*s_vectors)
    if swap_xy:
        xv, yv = yv, xv
    plotting.circle(xv, yv, fill_color = None, line_color=color, line_alpha=alpha, line_width=0.5, radius=radius, radius_units='screen')

class ColorBar(object):

    def __init__(self, scale, colorscale, continuous=True):
        self.scale = scale
        self.continuous = continuous

        self.colorscale = list(colorscale)
        for i, c in enumerate(self.colorscale):
            if isinstance(c, str):
                self.colorscale[i] = hex2rgb(c)
            self.colorscale[i] = np.array(self.colorscale[i])
        self.colorscale = tuple(self.colorscale)
        print(self.scale)

    def color(self, x):
        if self.continuous:
            if x <= self.scale[0]:
                return rgb2hex(self.colorscale[0])
            if x >= self.scale[-1]:
                return rgb2hex(self.colorscale[-1])
            index = bisect.bisect_left(self.scale, x) - 1
            c_a = self.colorscale[index]
            c_b = self.colorscale[index+1]
            c = ((x-self.scale[index])*c_b + (self.scale[index+1]-x)*c_a)/(self.scale[index+1]-self.scale[index])
            return rgb2hex(c)
        else:
            raise NotImplementedError


def bokeh_mesh_density(meshgrid, s_vectors=(), s_goals=(), swap_xy=True,
                       mesh_colors=('#DDDDDD', '#BBBBBB', '#999999', '#777777', '#555555'), title='no title',
                       e_radius=1.0, e_color=E_COLOR, e_alpha=0.75,
                       g_radius=1.0, g_color=G_COLOR, g_alpha=0.75, x_range=None, y_range=None, **kwargs):

    x_range, y_range = ranges(s_channels, x_range=x_range, y_range=y_range)
    xm = zip(*[b.bounds[0] for b in meshgrid.nonempty_bins])
    ym = zip(*[b.bounds[1] for b in meshgrid.nonempty_bins])
    if swap_xy:
        x_range, y_range = y_range, x_range
        xm, ym = ym, xm

    d_max = max(len(b) for b in meshgrid.nonempty_bins)
    mesh_scale = [1.0+i/(len(mesh_colors)-1)*d_max for i in range(len(mesh_colors))]
    colorbar = ColorBar(mesh_scale, mesh_colors, continuous=True)

    color = []
    for b in meshgrid.nonempty_bins:
        color.append(colorbar.color(len(b)))

    plotting.rect((np.array(xm[1])+np.array(xm[0]))/2   , (np.array(ym[1])+np.array(ym[0]))/2,
                  (np.array(xm[1])-np.array(xm[0]))*0.97, (np.array(ym[1])-np.array(ym[0]))*0.97,
                  #x_range=env.s_channels[0].bounds, y_range=env.s_channels[1].bounds,
                  x_range=x_range, y_range=y_range,
                  fill_color=color, fill_alpha=0.5,
                  line_color='#444444', line_alpha=0.0, title=title)
    plotting.hold(True)
    plotting.grid().grid_line_color='white'
    spread(meshgrid.s_channels, s_vectors=s_vectors, s_goals=s_goals, swap_xy=swap_xy,
           e_radius=e_radius, e_color=e_color, e_alpha=e_alpha,
           g_radius=g_radius, g_color=g_color, g_alpha=g_alpha)
    plotting.hold(False)

    plotting.hold(False)


def plotting_axis():
    plotting.xaxis().minor_tick_line_color = None
    plotting.xaxis().major_tick_in = 0
    plotting.yaxis().minor_tick_line_color = None
    plotting.yaxis().major_tick_in = 0


def perf_std(ticks, avgs, stds, **kwargs):
    if stds is not None:
        stds = [(s, s) for s in stds]
    return perf_astd(ticks, avgs, stds, **kwargs)

bokeh_stds = perf_std


def perf_astd(ticks, avgs, astds, color=BLUE, alpha=1.0, sem=1.0,
              plot_width=1000, plot_height=500, **kwargs):
    plotting.line(ticks, avgs, color=color, line_alpha=alpha, title_text_font_size= '6pt',
                  plot_width=plot_width, plot_height=plot_height, **kwargs)
    plotting.hold(True)

    if astds is not None:
        x_std = list(ticks) + list(reversed(ticks))
        y_std = (             [a - s_min/math.sqrt(sem) for a, (s_min, s_max) in zip(avgs, astds)] +
                list(reversed([a + s_max/math.sqrt(sem) for a, (s_min, s_max) in zip(avgs, astds)])))
        plotting.patch(x_std, y_std, fill_color=color, fill_alpha=alpha*0.25, line_color=None)
    plotting.grid().grid_line_color = 'white'
    plotting_axis()

    plotting.hold(False)

bokeh_astds = perf_astd


def bokeh_quantiles(ticks, avgs, quantiles, color='#000055', alpha=1.0, **kwargs):
    plotting.line(ticks, avgs, color=color, line_alpha=alpha, title_text_font_size= '6pt', **kwargs)
    plotting.hold(True)

    if quantiles is not None:
        print(quantiles)
        x_std = list(ticks) + list(reversed(ticks))
        y_std = (             [q_min for q_min, q_max in quantiles] +
                list(reversed([q_max for q_min, q_max in quantiles])))
        plotting.patch(x_std, y_std, fill_color=color, fill_alpha=alpha*0.25, line_color=None)
    plotting.grid().grid_line_color = 'white'
    plotting_axis()

    plotting.hold(False)


def perf_std_discrete(ticks, avgs, stds, legend=None,
                      std_width=0.3, plot_width=1000, plot_height=300,
                      color=BLUE, alpha=1.0, **kwargs):
    plotting.rect(ticks, avgs, [std_width for _ in stds], 2*np.array(stds),
                  line_color=None, fill_color=color, fill_alpha=alpha*0.5,
                  plot_width=plot_width, plot_height=plot_height, **kwargs)
    plotting.hold(True)
    plotting.line(ticks, avgs, line_color=color, line_alpha=alpha, legend=legend)
    plotting.circle(ticks, avgs, line_color=None, fill_color=color, fill_alpha=alpha)
    plotting.grid().grid_line_color = 'white'
    plotting_axis()

    plotting.hold(False)




if __name__ == '__main__':
    print(rgb2hex((37, 119, 178)))
    print(hex2rgb(rgb2hex((37, 119, 178))))
    import numpy as np
    print(np.array(rgba2rgb((255, 255, 255), (166, 48, 28, 0.50)))/255.0)
