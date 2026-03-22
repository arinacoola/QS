import math
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator

def standard_toffoli_unitary_article() -> np.ndarray:
    mat = np.eye(8, dtype=complex)
    mat[6, 6] = 0.0
    mat[7, 7] = 0.0
    mat[6, 7] = 1.0
    mat[7, 6] = 1.0
    return mat

def margolus_unitary_article() -> np.ndarray:
    mat = np.zeros((8, 8), dtype=complex)
    for i in range(4):
        mat[i, i] = 1.0
    mat[4, 4] = 1.0
    mat[5, 5] = -1.0
    mat[6, 7] = 1.0
    mat[7, 6] = 1.0
    return mat

def reverse_bits(x: int, n: int) -> int:
    s = format(x, f"0{n}b")
    return int(s[::-1], 2)

def article_to_qiskit_basis(mat: np.ndarray) -> np.ndarray:
    dim = mat.shape[0]
    n = int(round(math.log2(dim)))
    out = np.zeros_like(mat, dtype=complex)
    for i in range(dim):
        for j in range(dim):
            out[reverse_bits(i, n), reverse_bits(j, n)] = mat[i, j]

    return out

def matrix_as_gate(label: str, matrix_article: np.ndarray) -> Gate:
    matrix_qiskit = article_to_qiskit_basis(matrix_article)
    return UnitaryGate(matrix_qiskit, label=label)

def toffoli_gate() -> Gate:
    return matrix_as_gate("Toff", standard_toffoli_unitary_article())

def margolus_gate_from_matrix() -> Gate:
    return matrix_as_gate("Marg", margolus_unitary_article())

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
    circ1.append(toffoli_gate(), [0, 1, 2])
    print("standard Toffoli gate:")
    print(circ1.draw("text"))
    print()
    circ2 = QuantumCircuit(3)
    circ2.append(margolus_gate_from_matrix(), [0, 1, 2])
    print("Margolus gate as a matrix:")
    print(circ2.draw("text"))
    print()
    circ3 = QuantumCircuit(3)
    circ3.append(margolus_gate_from_decomposition(), [0, 1, 2])
    print("Margolus gate as a decomposition:")
    print(circ3.decompose().draw("text"))
    print()

def check_margolus_phase_equivalence():
    matrix_gate = margolus_gate_from_matrix()
    decomp_gate = margolus_gate_from_decomposition()
    op_matrix = Operator(matrix_gate).data
    op_decomp = Operator(decomp_gate).data
    diff = op_decomp @ op_matrix.conj().T
    is_diagonal = np.allclose(diff, np.diag(np.diag(diff)))
    unit_phases = np.allclose(np.abs(np.diag(diff)), np.ones(8))
    print("equivalent up to diagonal phase factors:",
          is_diagonal and unit_phases)

def print_gate_action_on_basis_article():
    toffoli_matrix = standard_toffoli_unitary_article()
    margolus_matrix = margolus_unitary_article()
    basis_states = [format(i, "03b") for i in range(8)]
    print("action of the Toffoli gate (article basis):")
    for i, ket in enumerate(basis_states):
        col = toffoli_matrix[:, i]
        target_index = np.argmax(np.abs(col))
        print(f"|{ket}> -> |{basis_states[target_index]}>")
    print()
    print("action of the Margolus gate (article basis):")
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
    check_margolus_phase_equivalence()
    print_gate_action_on_basis_article()