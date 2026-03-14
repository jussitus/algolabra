from delaunay import delaunay
import random

s = set()
random.seed(42)
for i in range(0,1000):
    s.add((random.randint(0,200),random.randint(0,200)))
s = sorted(s)
#print(s)

d = delaunay(s)[0]
print(d)
for i in range(1,10):
    d = d.lnext
    print(f'lnext {i}: {d}')
