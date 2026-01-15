import matplotlib.pyplot as plt
import numpy as np
import scipy

def filter(R, V, x):

    n = (1 - 2*R + R**2) * V
    d = 1 - 2*R*V*np.cos(2*np.pi*x) + (R*V)**2
    return n / d


def plt_filter(x, T1, T2, R, n, fn=None):
    plt.figure(figsize=(16, 6))
    ax = plt.gca()

    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    plt.xticks(np.arange(0, n+1))
    plt.yticks([0, 0.5, 1.0])
    #plt.xlim(0, n)
    plt.ylim(0, 1.5)

    one = np.ones(len(x))
    low = np.ones(len(x)) * ((1-R) / (1+R))**2
    plt.plot(x, one, "k")
    plt.plot(x, low, "k")
    plt.plot(x, T1, "b")
    plt.plot(x, T2, "r")

    if fn:
        plt.savefig(fn)


nx = 500
n = 3
R = 0.7

x = 0.5 + np.arange(n*nx) / nx
T1 = filter(R, 1.0, x) # max = 1
T2 = filter(R, 1.0/R, x) # max = infinite
#T2 = filter(R, 1.0/R**2, x) # max = 1

plt_filter(x, T1, T2, R, n, "filter.svg")

plt.show()
