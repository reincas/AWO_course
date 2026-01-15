import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp

colormap = "coolwarm"
radius = 4

def plot_heatmap(x, y, data, mode, cmap=colormap):
    plt.figure(figsize=(6, 5))
    plt.contourf(x, y, data, 50, cmap=cmap, vmin=-1, vmax=1)
    #plt.colorbar(label='Field Magnitude')
    #plt.title(f"Heatmap of Field Magnitude for {mode} Mode")
    #plt.xlabel("Width (a)")
    #plt.ylabel("Height (b)")
    #plt.axis('equal')
    ax = plt.gca()
    ax.set_aspect(1)
    ax.axis('off')
    plt.savefig(f"contour_{mode}.png", dpi=200, bbox_inches='tight', pad_inches=0)
    plt.show()
    plt.close()

def calculate_field(x, y, l, m):

    r = np.sqrt(x**2 + y**2)
    phi = np.atan2(y, x)

    u = sp.jn_zeros(l, m)[-1]
    field = np.cos(l * phi) * sp.jv(l, u*r/radius)
    field /= np.max(field)
    field = np.where(r > radius, 0.0, field)
    return field

x = np.linspace(-radius, radius, 200*radius)
y = np.linspace(-radius, radius, 200*radius)
x, y = np.meshgrid(x, y)

modes = {
    "LP01": (0, 1),
    "LP02": (0, 2),
    "LP03": (0, 3),
    "LP11": (1, 1),
    "LP12": (1, 2),
    "LP13": (1, 3),
    "LP23": (2, 3),
}

for mode, (m, n) in modes.items():
    field = calculate_field(x, y, m, n)
    plot_heatmap(x, y, field, mode)