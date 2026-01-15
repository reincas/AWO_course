import matplotlib.pyplot as plt
import numpy as np
import scipy

def gamma(E, n_tau):

    nt = len(E) - n_tau
    return [np.sum(y[0:nt] * y[tau:tau+nt:])/nt for tau in range(n_tau)]


def contrast(E, n_tau):

    g = gamma(E, n_tau)
    return g / g[0]


def plt_fields(dx, f0, x, y, y_sum, fn=None):
    plt.figure(figsize=(16, 6))
    ax = plt.gca()

    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    plt.xticks(np.arange(0, dx, 1 / f0))
    plt.yticks([-1.0, -0.5, 0, 0.5, 1.0])
    plt.xlim(0, dx)

    zero = np.zeros(len(x))
    plt.plot(x, zero, "k")
    plt.plot(x, y_sum, "r", linewidth=3.0)
    plt.plot(x, y[:, 0], "m")
    plt.plot(x, y[:, 1], color="orange")
    plt.plot(x, y[:, 2], "b")

    if fn:
        plt.savefig(fn)


def plt_contrast(dx, f0, u, v, fn=None):
    plt.figure(figsize=(16, 12))
    ax = plt.gca()

    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    plt.xticks(np.arange(0, dx, 1 / f0))
    plt.yticks([-1.0, -0.5, 0, 0.5, 1.0])
    plt.xlim(0, dx)

    zero = np.zeros(len(u))
    e = np.ones(len(u)) / np.e
    plt.plot(u, zero, "k")
    plt.plot(u, e, "k")
    plt.plot(u, np.abs(v), "r")
    plt.plot(u, v, "b")

    if fn:
        plt.savefig(fn)

dx = 500
nx = 200 * dx
nf = 3

x = np.arange(nx)
f0 = 15 / dx
df = 0.045 * f0
f = np.linspace(f0-0.5*df, f0+0.5*df, nf)
ff, xx = np.meshgrid(f, x)
y = np.cos(2*np.pi*ff*xx)
y_sum = np.sum(y, axis=1) / nf

v = contrast(y_sum, dx)
u = np.arange(dx)

plt_fields(dx, f0, x, y, y_sum, "fields.svg")
plt_contrast(dx, f0, u, v, "contrast.svg")

plt.show()
