import math
from random import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_genarator.distribution import Multi_Gauss_distribution, Triangle_distribution, Log_distribution, \
    Exp_distribution, Flat_distribution


def generate_points_from_distribution(no_of_points, dist, x_min, x_max, y_max):
    points = []
    size = no_of_points
    p = 0
    while p < size:
        x = x_min + random() * (x_max - x_min);
        y = random() * y_max
        if (y <= dist.d(x)):
            p += 1
            points.append(x)
    return points

def save_as_png(points, x_min, x_max, name):
    fig = plt.figure()
    plt.title(name + ' historam')
    plt.xlabel('x')
    plt.ylabel('count')
    bin_width = (x_max-x_min)/75
    bins = []
    actual = x_min - bin_width / 2
    while actual < x_max:
        bins.append(actual)
        actual += bin_width
    plt.hist(points, bins=bins, label='hist')
    plt.savefig("../_data/out/distributions/"+name+'.png')

def dist_as_png(fun, x_min, x_max, period, shift, name):
    print(name, x_min, x_max)
    fig = plt.figure()
    plt.title('Probability distribution '+name)
    plt.xlabel('x')
    plt.ylabel('g(x)')
    x = np.array(range(0,100))
    x = x*(x_max-x_min)/100+x_min
    y = fun(x)
    scale_factor = period/max
    x= (scale_factor*x + shift)%period
    plt.plot(x, y)
    plt.savefig("../_data/out/distributions/dist_"+name+'.png')

def dist_as_png(dist, x_min, x_max, period, shift, name):
    print(name, x_min, x_max)
    fig = plt.figure()
    plt.title('Probability distribution '+name)
    plt.xlabel('x')
    plt.ylabel('g(x)')
    print(name)
    print("_s", x_max, x_min)
    x = np.array(range(0,100))
    x = x*(x_max-x_min)/100+x_min
    fun = np.vectorize(dist.d)
    y = fun(x)
    scale_factor = period/x_max
    x = (x*scale_factor+shift)%period
    plt.plot(x, y)
    plt.savefig("../_data/out/distributions/dist_pdf_"+name+'.png')


def save_as_csv(points, name):
    dF = pd.DataFrame(points);
    dF.to_csv("../_data/out/distributions/"+name+'.csv', sep=";", header=False, index=False)

def generate_uniform_gauss_parameters(modals, factor, min_mean, max_mean, sigma):
    factors = []
    means = []
    sigmas = []
    mean_dist = (max_mean-min_mean)/(modals-1)
    for m in range(modals):
        factors.append(factor)
        means.append(m*mean_dist+min_mean)
        sigmas.append(sigma)
    return factors, means, sigmas

def save_distribution(name, number_of_modals, points, dist, min, max, period, shift):
    name = "{0}{1}_{2}".format(number_of_modals,name, shift)
    dist_as_png(dist, min, max, period, shift, name)
    scale_factor = period/max
    _points = points.copy()
    _points = (_points*scale_factor+shift)%period
    save_as_png(_points, scale_factor*min, period, name)
    save_as_csv(_points, name)
    return _points


def generate_multi_modal_gauss():
    points_per_peek = 3000

    y_max =2

    #factors, means, sigmas = generate_uniform_gauss_parameters(number_of_modals, factor=5, min_mean=5, max_mean=15, sigma=1.5)
    factors = [5, 1, 1, 5]
    means = [10.0, 20.0, 30.0, 40.0 ]
    sigmas = [3, 3, 3, 3]
    number_of_modals = len(factors)
    print("Factors", factors)
    print("means", means)
    print("sigmas",sigmas)
    dist = Multi_Gauss_distribution(factors, means, sigmas)
    print(factors, means, sigmas)
    x_min = 0;
    x_max = 10 * (number_of_modals + 1)
    points = np.array(generate_points_from_distribution(points_per_peek * number_of_modals, dist, x_min, x_max, y_max))
    data = pd.DataFrame()
    _p = save_distribution("modal_gaus", number_of_modals, points, dist, min=0, max=50, period=360, shift=0)
    data['base'] = _p
    _p = save_distribution("modal_gaus", number_of_modals, points, dist, min=0, max=50, period=360, shift=90)
    data['90'] = _p
    #_p = save_distribution("modal_gaus", number_of_modals, points, dist, min=0, max=50, period=360, shift=160)
    #data['base'] = _p
    _p = save_distribution("modal_gaus", number_of_modals, points, dist, min=0, max=50, period=360, shift=280)
    data['280'] = _p
    data.to_csv("../_data/out/distributions/modal_gauss.csv", sep=';')
    print('done')



generate_multi_modal_gauss()