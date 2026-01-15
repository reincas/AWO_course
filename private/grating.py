import math

a0 = 70 * math.pi/180
a1 = 25 * math.pi/180

L = math.sin(a0) - math.sin(a1)
mmin = math.ceil((math.sin(a0)-1)/L)
mmax = math.floor((math.sin(a0)+1)/L)
for m in range(mmin, mmax+1):
    am = math.asin(math.sin(a0) - m*L) * 180/math.pi
    print(f"{+m}: {am:.3f}")