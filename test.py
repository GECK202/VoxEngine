import numpy as nu
import time

VC = 32768
CH = 10000
t = time.perf_counter()
ch = [0]*CH
for i in range(CH):
    ch[i] = [0.0]*VC
#print(ch)
nt = time.perf_counter()
dt = nt - t
print("list1 =",dt)

t = time.perf_counter()
ch = list(range(CH))
for i in range(CH):
    ch[i] = [0.0]*VC
#print(ch)
nt = time.perf_counter()
dt = nt - t
print("list2 =",dt)

t = time.perf_counter()
ch = nu.zeros(CH, dtype=object)
for i in range(CH):
    ch[i] = nu.zeros(VC, dtype=nu.float32)
#print(ch)
nt = time.perf_counter()
dt = nt - t
print("ndarray =",dt)


