import cirq
import time
import math
import matplotlib.pyplot as plt

def mark_one(cir,qubt, target):
    bits =target[::-1]
    for i, bit in enumerate(bits):
        if bit == "0":
            cir.append(cirq.X(qubt[i]))
    cir.append(cirq.Z(qubt[-1]).controlled_by(*qubt[:-1]))
    for i, bit in enumerate(bits):
        if bit == "0":
            cir.append(cirq.X(qubt[i]))

def diff(cir,qubt):
    cir.append(cirq.H.on_each(*qubt))
    cir.append(cirq.X.on_each(*qubt))
    cir.append(cirq.Z(qubt[-1]).controlled_by(*qubt[:-1]))
    cir.append(cirq.X.on_each(*qubt))
    cir.append(cirq.H.on_each(*qubt))

def grover(n, target):
    qubt=cirq.LineQubit.range(n)
    cir=cirq.Circuit()
    cir.append(cirq.H.on_each(*qubt))
    N = 2 **n
    steps = round(math.pi/4*math.sqrt(N)-0.5) 
    steps=max(1, steps) 
    for _ in range(steps):
        mark_one(cir, qubt, target)
        diff(cir,qubt)
    cir.append(cirq.measure(*qubt, key="result"))
    return cir

sizes=[]
times =[]
sim=cirq.Simulator()
rep =100 

for n in range(2,11):
    target = "1"*n
    cir =grover(n, target)
    start=time.perf_counter()
    result = sim.run(cir,repetitions=rep)
    end = time.perf_counter()
    N=2**n
    elapsed =(end - start)/rep
    sizes.append(N)
    times.append(elapsed)
    print("n =", n, "N =", N, "time =", round(elapsed, 4), "sec")

plt.plot(sizes,times,marker="o")
plt.xlabel("number of elements N")
plt.ylabel("average  execution time, sec")
plt.title("Grover algorithm simulation time")
plt.grid(True)
plt.savefig("grover_time.png")
plt.show()