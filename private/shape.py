import numpy as np
import matplotlib.pyplot as plt

h0 = 15
a0 = 1.0
b0 = 2 * np.pi / 16
p0 = 0.0

h1 = 5
b1 = 2 * np.pi / 40
p1 = np.atan(b1/b0 * np.tan(b0*h0/2 + p0)) - b1*h0/2
a1 = a0*np.sin(b0*h0/2 + p0) / np.sin(b1*h0/2 + p1)
print(a1/a0)

# Definition der Teilbereiche
x1 = np.linspace(-h0/2-h1, -h0/2, 500)
x2 = np.linspace(-h0/2, h0/2, 1000)
x3 = np.linspace(h0/2, h0/2+h1, 500)

# Definition der stückweise definierten Funktion
y1 = a1 * np.sin(b1 * x1 - p1)
y2 = a0 * np.sin(b0 * x2 + p0)
y3 = a1 * np.sin(b1 * x3 + p1)

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
