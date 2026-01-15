import matplotlib.pyplot as plt
import numpy as np
import scipy

# Slit distance in multiples of the wavelength
a = 60

# Slit width in multiples of the wavelength
b = 12

# Distance of the screen
z = 600

# Maximum x value on the screen in multiples of the wavelength
xmax = 160

# Number of data points is 2*nx+1
nx = 500

def intensity(x, a, b):
    alpha = np.arctan2(x, z)
    return (np.sinc(b*np.sin(alpha)) * np.cos(np.pi*a*np.sin(alpha)))**2


def plt_interferogram(x, I0, I, fn=None):
    plt.figure(figsize=(16, 6))
    ax = plt.gca()

    #ax.axes.xaxis.set_ticklabels([])
    #ax.axes.yaxis.set_ticklabels([])
    #plt.xticks(np.arange(0, dx, 1 / f0))
    plt.yticks([0, 0.5, 1.0])
    #plt.xlim(-40, 40)

    zero = np.zeros(len(x))
    plt.plot(x, zero, "k")
    plt.plot(x, I, "r", linewidth=3.0)
    plt.plot(x, I0, "k", linewidth=3.0)

    if fn:
        plt.savefig(fn)

x = xmax * (np.arange(2*nx+1) / nx - 1)
I = intensity(x, a, b)
I0 = intensity(x, 0, b)

plt_interferogram(x, I0, I, "doubleslit.svg")

plt.show()
