# Source:
# https://physics.stackexchange.com/questions/801416/unbound-states-of-the-1d-finite-potential-well

import numpy as np
import matplotlib.pyplot as plt

L = 15
A = 1.0
k = 2 * np.pi / 100000
n = 2 * np.pi / 12
pEven = False

# Definition der Teilbereiche
x1 = np.linspace(-2*L, -L/2, 1500)
x2 = np.linspace(-L/2, L/2, 1000)
x3 = np.linspace(L/2, 2*L, 1500)

# Definition der stückweise definierten Funktion
if pEven:
    C = A * (n/k * np.sin(n*L/2) * np.sin(k*L/2) + np.cos(n*L/2) * np.cos(k*L/2))
    D = A * (n/k * np.sin(n*L/2) * np.cos(k*L/2) - np.cos(n*L/2) * np.sin(k*L/2))
    y1 = C * np.cos(k*x1) + D * np.sin(k*x1)
    y2 = A * np.cos(n*x2)
    y3 = C * np.cos(k*x3) - D * np.sin(k*x3)
else:
    C = A * (n/k * np.cos(n*L/2) * np.sin(k*L/2) - np.sin(n*L/2) * np.cos(k*L/2))
    D = A * (n/k * np.cos(n*L/2) * np.cos(k*L/2) + np.sin(n*L/2) * np.sin(k*L/2))
    y1 = C * np.cos(k*x1) + D * np.sin(k*x1)
    y2 = A * np.sin(n*x2)
    y3 = -C * np.cos(k*x3) + D * np.sin(k*x3)

# Plotten der Funktion
plt.figure(figsize=(10, 5))
plt.plot(x1, y1, label='Bereich A')
plt.plot(x2, y2, label='Bereich B')
plt.plot(x3, y3, label='Bereich C')

# Gestaltung
plt.title('Stückweise definierte Funktion y = A * sin(bx + p)')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)

# Anzeige
plt.tight_layout()
plt.show()
