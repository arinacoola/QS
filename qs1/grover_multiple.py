import cirq
import math

def mark_one(cir,qubt,target):
    bits=target
    for i, bit in enumerate(bits):
        if bit == "0":
            cir.append(cirq.X(qubt[i]))
    cir.append(cirq.Z(qubt[-1]).controlled_by(*qubt[:-1]))
    for i, bit in enumerate(bits):
        if bit == "0":
            cir.append(cirq.X(qubt[i]))

def oracle(cir,qubt, targets):
    for target in targets:
        bits=target
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

def grover_many(n, targets):
    qubt=cirq.LineQubit.range(n)
    cir = cirq.Circuit()
    cir.append(cirq.H.on_each(*qubt))
    N=2 ** n
    k=len(targets)
    theta = math.asin(math.sqrt(k/N))
    steps = round(math.pi /(4 * theta) - 0.5)
    steps =max(1,steps)
    print("iter: ",steps)
    for _ in range(steps):
        oracle(cir,qubt,targets)
        diff(cir,qubt)
    cir.append(cirq.measure(*qubt,key="result"))
    return cir

n=3
targets=["101", "011"]
cir=grover_many(n, targets)
print(cir)
sim =cirq.Simulator()
result=sim.run(cir, repetitions=1000)
print(result.histogram(key="result"))