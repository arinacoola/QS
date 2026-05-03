import cirq
import math

def state(cir,qubt,target):
    bits = target[::-1]
    for i, bit in enumerate(bits):
        if bit == "0":
            cir.append(cirq.X(qubt[i]))
    cir.append(cirq.Z(qubt[-1]).controlled_by(*qubt[:-1]))
    for i, bit in enumerate(bits):
        if bit == "0":
            cir.append(cirq.X(qubt[i]))

def diff(cir, qubt):
    cir.append(cirq.H.on_each(*qubt))
    cir.append(cirq.X.on_each(*qubt))
    cir.append(cirq.Z(qubt[-1]).controlled_by(*qubt[:-1]))
    cir.append(cirq.X.on_each(*qubt))
    cir.append(cirq.H.on_each(*qubt))

def grover(n,target):
    qubt = cirq.LineQubit.range(n)
    cir=cirq.Circuit()
    cir.append(cirq.H.on_each(*qubt))
    N = 2 ** n
    steps = round(math.pi/4 *math.sqrt(N) - 0.5) 
    steps =max(1,steps)  
    for _ in range(steps):
        state(cir,qubt,target)
        diff(cir,qubt)
    cir.append(cirq.measure(*qubt, key="result"))
    return cir

n = 3
target = "101"
cir=grover(n,target)
print(cir)
sim = cirq.Simulator()
result = sim.run(cir,repetitions=1000)
print(result.histogram(key="result"))