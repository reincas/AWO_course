import math

a = 20
b = 3.95
dx = 4


for x in range(13):
    ya = a * math.exp(-(x + dx) ** 2 / b ** 2) + a * math.exp(-(x - dx) ** 2 / b ** 2)
    yb = a * math.exp(-(x + dx) ** 2 / b ** 2) - a * math.exp(-(x - dx) ** 2 / b ** 2)
    print(f"{x:2d} {ya:3.0f} {yb:3.0f}")