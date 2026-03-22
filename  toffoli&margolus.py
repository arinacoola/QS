import math
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from qiskit.quantum_info import Operator


def basis_state(index: int, dim: int) -> np.ndarray:
    vec = np.zeros((dim, 1), dtype=complex)
    vec[index, 0] = 1.0
    return vec @ vec.conj().T

def standard_toffoli_unitary() -> np.ndarray:
    mat = np.eye(8, dtype=complex)
    mat[6, 6] = 0.0
    mat[7, 7] = 0.0
    mat[6, 7] = 1.0
    mat[7, 6] = 1.0
    return mat

def margolus_unitary() -> np.ndarray:
    mat = np.zeros((8, 8), dtype=complex)
    for i in range(4):
        mat[i, i] = 1.0
    mat[4, 4] = 1.0
    mat[5, 5] = -1.0
    mat[6, 7] = 1.0
    mat[7, 6] = 1.0
    return mat


def matrix_as_gate(label: str, matrix: np.ndarray) -> Gate:
    return Operator(matrix).to_instruction(label=label)

def toffoli_gate() -> Gate:
    return matrix_as_gate("Toff", make_standard_toffoli_unitary())

def margolus_gate_from_matrix() -> Gate:
    return matrix_as_gate("Marg", make_margolus_unitary())

def margolus_gate_from_decomposition() -> Gate:
    circ = QuantumCircuit(3, name="Marg_dec")
    angle = math.pi / 4
    circ.ry(angle, 2)
    circ.cx(1, 2)
    circ.ry(angle, 2)
    circ.cx(0, 2)
    circ.ry(-angle, 2)
    circ.cx(1, 2)
    circ.ry(-angle, 2)
    return circ.to_gate()

def display_gate_circuits():
    circ1 = QuantumCircuit(3)
    circ1.append(make_toffoli_gate(), [0, 1, 2])
    print("standard Toffoli gate: ")
    print(circ1.draw("text"))
    print()
    circ2 = QuantumCircuit(3)
    circ2.append(make_margolus_gate_from_matrix(), [0, 1, 2])
    print("the Margolus gate as a matrix: ")
    print(circ2.draw("text"))
    print()
    circ3 = QuantumCircuit(3)
    circ3.append(make_margolus_gate_from_decomposition(), [0, 1, 2])
    print("the Margolus gate as a schedule: ")
    print(circ3.draw("text"))
    print()

def check_margolus_consistency():
    op_a = Operator(make_margolus_gate_from_matrix())
    op_b = Operator(make_margolus_gate_from_decomposition())
    same = np.allclose(op_a.data, op_b.data)
    print("coincidence of two Margolus implementations: ", same)

def print_gate_action_on_basis():
    toffoli_matrix = make_standard_toffoli_unitary()
    margolus_matrix = make_margolus_unitary()
    basis_states = [format(i, "03b") for i in range(8)]
    print("The principle of the Tofoli gate: ")
    for i, ket in enumerate(basis_states):
        col = toffoli_matrix[:, i]
        target_index = np.argmax(np.abs(col))
        print(f"|{ket}> -> |{basis_states[target_index]}>")
    print()
    print("The principle of the  Margolus gate: ")
    for i, ket in enumerate(basis_states):
        col = margolus_matrix[:, i]
        target_index = np.argmax(np.abs(col))
        amplitude = col[target_index]
        if np.isclose(amplitude, 1):
            print(f"|{ket}> -> |{basis_states[target_index]}>")
        elif np.isclose(amplitude, -1):
            print(f"|{ket}> -> -|{basis_states[target_index]}>")
        else:
            print(f"|{ket}> -> {amplitude}|{basis_states[target_index]}>")
    print()

if __name__ == "__main__":
    display_gate_circuits()
    check_margolus_consistency()
    print_gate_action_on_basis()