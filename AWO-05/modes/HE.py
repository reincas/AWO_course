import numpy as np
import matplotlib.pyplot as plt

colormap = "coolwarm"
width = 4
height = 4

def plot_heatmap(x, y, data, mode, cmap=colormap):
    plt.figure(figsize=(6, 5))
    plt.contourf(x, y, data, 50, cmap=cmap, vmin=-1, vmax=1)
    #plt.colorbar(label='Field Magnitude')
    #plt.title(f"Heatmap of Field Magnitude for {mode} Mode")
    #plt.xlabel("Width (a)")
    #plt.ylabel("Height (b)")
    #plt.axis('equal')
    ax = plt.gca()
    ax.set_aspect(2/3)
    ax.axis('off')
    plt.savefig(f"contour_{mode}.png", dpi=200, bbox_inches='tight', pad_inches=0)
    plt.show()
    plt.close()

def calculate_field(x, y, m, n):

    ax = m / 2
    bx = width * ((m-1) % 2) / 4
    ay = n / 2
    by = height * ((n-1) % 2) / 4

    field = np.cos(2*np.pi * (ax*x+bx) / width) * np.cos(2*np.pi * (ay*y+by) / height)
    return field

x = np.linspace(-width/2, width/2, 100*width)
y = np.linspace(-height/2, height/2, 100*height)
x, y = np.meshgrid(x, y)

modes = {
    "HE11": (1, 1),
    "HE12": (1, 2),
    "HE13": (2, 1),
    "HE21": (2, 2),
    "HE22": (3, 1),
    "HE23": (3, 2),
}

for mode, (m, n) in modes.items():
    field = calculate_field(x, y, m, n)
    plot_heatmap(x, y, field, mode)