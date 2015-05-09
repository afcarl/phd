from __future__ import division

import math

import numpy as np
import shapely

from environments import tools
import learners
from clusterjobs import datafile

import paths
import gfx

# # Seeds generated with python 2.7.6
# import random, sys
# random.seed(1442695040888963407)
# # with sys.maxint == 9223372036854775807
# seeds = [random.randint(0, 9223372036854775807) for _ in range(100)]
seeds = [2277780588542364672, 2271847692760035822, 6778297736022969453, 731488599360964631, 2249919185132747185, 2144127347946942260, 7849293421982753909, 3163449819090479779, 7414795688107581286, 915874242295682013, 2951282313904607239, 5252322767729632796, 7902141969472472752, 8631535590479184973, 5286088901037173646, 5491604618789231439, 3719653349859327011, 6819081996980257238, 1748658351415132242, 8812816375084936578, 6886837323949936464, 4480791189190677684, 1514256279926678348, 7229313889129282454, 1875013125129091478, 7417705637407443469, 3885803598318672902, 4691886924882846616, 5112577389355631693, 8926167187416095763, 4622864596063186145, 1685462565235781081, 4772648093271016255, 2941940404039447517, 733168485598614026, 6463677590872578646, 8545482801734283751, 7476636053416677518, 6800435324154081300, 8750176894817286174, 1471235916864798866, 3206910568272184629, 4977470622003665215, 3563008650483435977, 6148242523002971361, 6735323964533659717, 742255496523260973, 2563467239626128696, 8256914428336670893, 8914241828351143632, 3852067938229836075, 2591418156226478074, 1623480749567091802, 7947390936384784888, 329320166120307642, 7586990055608418230, 7119372721358905008, 5224523738475875941, 6068298529865207740, 8896952298357669385, 2978230742926299244, 7664533960211457662, 1048929589916666960, 6767798515199187048, 6827365698219288839, 719319643530290657, 4165744513094059215, 5925558893415775557, 7835567919366619410, 8884310663761083929, 1842090387816173463, 2134648298637590214, 2738729883249125284, 5655061056732731688, 7800877190195507658, 4482408863398176908, 7703735483001282360, 4141445236401549670, 6656103186966871953, 3305189591782918675, 5951012370168624126, 1057150275611764442, 8117940878272915740, 6784428635851078714, 28834552707735084, 363666429385335711, 3047049233616075062, 6685578736860479494, 4902434180781310790, 8527662131338660266, 8721944426378116550, 2567105574385898872, 7894750954147039687, 1242599956128329760, 9135887815263181481, 7419870817221424311, 370608609155301312, 7776323607914860204, 2214947427214858440, 6001755323515175486]

def dist(p1, p2):
    return math.sqrt(sum((p1i-p2i)**2 for p1i, p2i in zip(p1, p2)))



_testset = None
def testset():
    global _testset
    if _testset is None:
        ts = datafile.load_file(paths.testset_filepath)
        _testset = tuple(tools.to_vector(s_signal, ts['s_channels']) for s_signal in ts['s_signals'])
    return _testset


def run_exploration(env, ex, N, mesh=None, verbose=True, prefix=''):
    explorations, s_vectors, s_goals = [], [], []

    for i in range(N):
        if verbose and i % 100 == 0:
            gfx.print_progress(i, N, prefix=prefix)
        exploration = ex.explore()
        feedback = env.execute(exploration['m_signal'])
        ex.receive(exploration, feedback)
        s_vectors.append(tools.to_vector(feedback['s_signal'], env.s_channels))
        if 's_goal' in exploration:
            s_goals.append(tools.to_vector(exploration['s_goal'], env.s_channels))
        if mesh is not None:
            mesh.add(feedback['s_signal'], m_signal=exploration['m_signal'])
        explorations.append((exploration, feedback))
    if verbose:
        gfx.print_progress(N, N, prefix=prefix)

    return explorations, s_vectors, s_goals


def run_nn(testset, s_vectors):

    nnset = learners.NNSet()
    for s_vector in s_vectors:
        nnset.add((), s_vector)

    errors = []
    for s_vector_goal in testset:
        distances, idx = nnset.nn_y(s_vector_goal, k=1)
        s_vector = nnset.ys[idx[0]]
        errors.append(dist(s_vector_goal, s_vector))

    return errors

def run_nns(testset, s_vectors, ticks=None, verbose=True):
    if ticks is None:
        ticks = range(len(s_vectors))
    ticks, N = set(ticks), len(ticks)


    avgs, stds = [], []
    nnset = learners.NNSet()
    for t, s_vector in enumerate(s_vectors):

        nnset.add((), s_vector)

        if t in ticks:
            if verbose:
                gfx.print_progress(len(avgs) , N)
            errors = []
            for s_vector_goal in testset:
                distances, idx = nnset.nn_y(s_vector_goal, k=1)
                s_vector = nnset.ys[idx[0]]
                errors.append(dist(s_vector_goal, s_vector))
            avgs.append(np.mean(errors))
            stds.append(np.std(errors))

    if verbose:
        gfx.print_progress(N, N)

    return avgs, stds


def run_coverage(threshold, s_vectors):
    union = shapely.ops.unary_union([shapely.geometry.Point(*sv_i).buffer(threshold)
                                     for sv_i in s_vectors])
    return union.area

def run_coverages(threshold, s_vectors, ticks=None):
    if ticks is None:
        ticks = range(len(s_vectors))
    ticks = set(ticks)

    union = shapely.geometry.MultiPolygon([])
    areas = [0.0]
    for t, s_vector in enumerate(s_vectors):
        union = union.union(shapely.geometry.Point(*s_vector).buffer(threshold))
        if t in ticks:
            areas.append(union.area)

    return areas

def percentile_mean(error_avgs, p=0.10):
    ms = []
    for errors in error_avgs:
        errors = sorted(errors)
        errors = errors[:int(len(errors)*p)]
        ms.append(np.average(errors))

    return ms

def compass_extrema(s_vectors):
    min_x, min_x_idx = float('+inf'), -1
    max_x, max_x_idx = float('-inf'), -1
    min_y, min_y_idx = float('+inf'), -1
    max_y, max_y_idx = float('-inf'), -1

    for i, (x, y) in enumerate(s_vectors):
        if x < min_x:
            min_x     = x
            min_x_idx = i

        if x > max_x:
            max_x     = x
            max_x_idx = i

        if y < min_y:
            min_y     = y
            min_y_idx = i

        if y > max_y:
            max_y     = y
            max_y_idx = i

    return {'min_x': min_x_idx, 'max_x': max_x_idx,
            'min_y': min_y_idx, 'max_y': max_y_idx}



thetas = tuple(i*math.pi/4 for i in range(8))

def spread_extrema(s_vectors, dirs=thetas):
    def proj(x, y, theta):
        return (  x*math.cos(theta)
                + y*math.sin(theta))

    records = [(float('-inf'), -1) for d in thetas]
    for i, (x, y) in enumerate(s_vectors):
        for j, theta in enumerate(thetas):
            d = proj(x, y, theta)
            if records[j][0] < d:
                records[j] = d, i

    return [idx for d, idx in records]

