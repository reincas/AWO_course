import numpy as np
import matplotlib.pyplot as plt

h0 = 16

a0 = 1.0
b0 = 2 * np.pi / 16
p0 = -0.05 * 2*np.pi

#h1 = 5
a1 = 0.6
b1 = 2 * np.pi / 6

print(a1/a0, b0/b1)
assert 1 < a1/a0 < b0/b1 or b0/b1 < a1/a0 < 1
p1 = np.asin(np.sqrt(((b1/b0)**2-(a0/a1)**2)/((b1/b0)**2-1)))
p0 = a1/a0 * np.sin(p1)

# Definition der Teilbereiche
x2 = np.linspace(-h0, 0, 1000)
x3 = np.linspace(0, h0, 1000)

# Definition der stückweise definierten Funktion
y2 = a0 * np.sin(b0 * x2 + p0)
y3 = a1 * np.sin(b1 * x3 + p1)

# Plotten der Funktion
plt.figure(figsize=(10, 5))
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
