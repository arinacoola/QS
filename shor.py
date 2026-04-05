import math
import random
from fractions import Fraction
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector

N = 15
COUNT_QUBITS = 4
WORK_QUBITS = 4

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def classical_order_mod_n(a: int, n: int = N) -> int:
    if gcd(a, n) != 1:
        raise ValueError(f"{a} is not coprime with {n}")
    r = 1
    value = a % n
    while value != 1:
        value = (value * a) % n
        r += 1
    return r

def permutation_matrix_mul_mod_15(multiplier: int) -> np.ndarray:
    if gcd(multiplier, 15) != 1:
        raise ValueError("multiplier must be coprime with 15")
    dim = 16
    mat = np.zeros((dim, dim), dtype=complex)
    for y in range(15):
        target = (multiplier * y) % 15
        mat[target, y] = 1.0
    mat[15, 15] = 1.0
    return mat

def compiled_modmul_gate(multiplier: int) -> UnitaryGate:
    return UnitaryGate(
        permutation_matrix_mul_mod_15(multiplier),
        label=f"*{multiplier} mod 15"
    )

def inverse_qft(qc: QuantumCircuit, qubits: list[int]) -> None:
    n = len(qubits)
    for i in range(n // 2):
        qc.swap(qubits[i], qubits[n - 1 - i])
    for j in range(n):
        for m in range(j):
            angle = -math.pi / (2 ** (j - m))
            qc.cp(angle, qubits[m], qubits[j])
        qc.h(qubits[j])

def build_order_finding_circuit(a: int) -> QuantumCircuit:
    if gcd(a, N) != 1:
        raise ValueError(f"{a} is not coprime with {N}")
    qc = QuantumCircuit(COUNT_QUBITS + WORK_QUBITS, name=f"ord_{a}_mod_15")
    count = list(range(COUNT_QUBITS))
    work = list(range(COUNT_QUBITS, COUNT_QUBITS + WORK_QUBITS))
    for q in count:
        qc.h(q)
    qc.x(work[0])
    for j in range(COUNT_QUBITS):
        multiplier = pow(a, 2 ** j, N)
        controlled_gate = compiled_modmul_gate(multiplier).control(1)
        qc.append(controlled_gate, [count[j]] + work)
    inverse_qft(qc, count)
    return qc


def counting_distribution(qc: QuantumCircuit) -> dict[str, float]:
    count = list(range(COUNT_QUBITS))
    sv = Statevector.from_instruction(qc)
    dist = sv.probabilities_dict(qargs=count)
    cleaned = {bits: prob for bits, prob in dist.items() if prob > 1e-12}
    return dict(sorted(cleaned.items(), key=lambda x: x[1], reverse=True))

def phase_from_bits(bits: str) -> float:
    return int(bits, 2) / (2 ** COUNT_QUBITS)

def recover_order_from_distribution(a: int, dist: dict[str, float]) -> int | None:
    for bits, _ in dist.items():
        phase = phase_from_bits(bits)
        frac = Fraction(phase).limit_denominator(N)
        denominator = frac.denominator
        for k in range(1, N + 1):
            r = denominator * k
            if pow(a, r, N) == 1:
                return r
    return None

def choose_random_coprimes_to_15(k: int = 3, seed: int = 42) -> list[int]:
    candidates = [a for a in range(2, N) if gcd(a, N) == 1]
    rng = random.Random(seed)
    return rng.sample(candidates, k)

def main():
    chosen = choose_random_coprimes_to_15(3, seed=42)
    print(f"chosen values a: {chosen}")
    print("find ord_15(a) for each of them\n")
    for a in chosen:
        print("=" * 60)
        print(f"a = {a}")
        print(f"gcd({a}, 15) = {gcd(a, 15)}")
        qc = build_order_finding_circuit(a)
        print("\ncircuit:")
        print(qc.draw("text"))
        dist = counting_distribution(qc)
        print("\nmost probable counting-register outputs:")
        for bits, prob in list(dist.items())[:8]:
            print(f"  {bits}   p = {prob:.6f}")
        estimated_r = recover_order_from_distribution(a, dist)
        true_r = classical_order_mod_n(a, 15)
        print(f"\nestimated ord_15({a}) = {estimated_r}")
        print(f"true ord_15({a}) = {true_r}")
        print(f"Check: {a}^{true_r} mod 15 = {pow(a, true_r, 15)}")
        print()

if __name__ == "__main__":
    main()
