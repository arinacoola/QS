import cirq
import time
from grover import grover
from grover_multiple import grover_many

sim=cirq.Simulator()
rep= 100 
print("n | single_time | multiple_time")

for n in range(2 ,9):
    target = "1"* n
    targets=["1" * n,"0" * n]
    cir1 = grover(n, target)
    start =time.perf_counter()
    sim.run(cir1, repetitions=rep)
    t1 = (time.perf_counter()-start)/rep
    cir2 = grover_many(n,targets)
    start =time.perf_counter()
    sim.run(cir2,repetitions=rep)
    t2 = (time.perf_counter()-start)/rep

    print(n, "|", round(t1, 4), "|", round(t2,4))