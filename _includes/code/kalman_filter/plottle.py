import numpy as np
import matplotlib.pyplot as plt
import time

from sys import stdin

HISTOGRAM = 1
LIST = 2

bool_is_true = lambda a: (a == 'true')
lisp_list_to_pylist = lambda a: eval(','.join(a[1:-1].split(' ')))

if __name__ == '__main__':

    refresh_seconds = 0.5

    name_count = 0
    figure_ids = {}
    figure_values = {}
    cast_fn = {}
    figure_type = {}

    lastplot_time = time.time()

    while True:
        name, value = stdin.readline().strip().split(',')
        if name not in figure_values.keys():
            figure_values[name] = []
            name_count += 1
            figure_ids[name] = name_count
            try:
                casted = float(value)
                cast_fn[name] = float
                figure_type[name] = HISTOGRAM
            except:
                if value in ('true', 'false'):
                    casted = (value)
                    cast_fn[name] = bool_is_true
                    figure_type[name] = HISTOGRAM
                elif value[0] == '(' and value[-1] == ')':
                    cast_fn[name] = lisp_list_to_pylist
                    figure_type[name] = LIST
                else:
                    # TODO this wasn't really parsed
                    cast_fn[name] = str

        figure_values[name].append(cast_fn[name](value))
        
        if time.time() - lastplot_time > refresh_seconds:
            for name in figure_ids.keys():
                if figure_type[name] == HISTOGRAM:
                    fig = plt.figure(figure_ids[name])
                    fig.clf()
                    plt.title("Histogram of %s" % name)
                    if cast_fn[name] == float:
                        plt.hist(figure_values[name], normed=True, bins=min(250, max(10, 1e-4*len(figure_values[name]))))
                    elif cast_fn[name] == bool_is_true:
                        plt.hist(figure_values[name], normed=False, bins=[-0.2, 0.2, 0.8, 1.2])
                        plt.xticks([0, 1], ['False', 'True'])
                        plt.xlim([-0.2, 1.2])
                    else:
                        raise Exception("unknown type")
                    plt.draw()
                    plt.show(block=False)
                elif figure_type[name] == LIST:
                    fig = plt.figure(figure_ids[name])
                    #fig.clf()
                    plt.title("Current value of %s" % name)
                    numplots = len(figure_values[name][-1])
#                    for ix in xrange(numplots):
#                        plt.subplot(1,numplots,ix)
#                        subvals = [f[ix] for f in figure_values[name]]
#                        plt.hist(subvals, normed=True, bins=min(250, max(10, 1e-4*len(subvals))))
                    plt.plot(np.arange(numplots), figure_values[name][-1], 'b', alpha=0.2)
                    plt.draw()
                    plt.show(block=False)

            lastplot_time = time.time()
