from qiskit import QuantumCircuit

def add_4bit_num():
    qc = QuantumCircuit(13)
    a = [0, 1, 2, 3]
    b = [4, 5, 6, 7]
    c = [8, 9, 10, 11, 12]
    for i in range(4):
        qc.ccx(a[i], b[i], c[i+1])
        qc.cx(a[i], b[i])
    for i in reversed(range(4)):
        qc.cx(c[i], b[i])
        qc.ccx(a[i], b[i], c[i+1])
    return qc

def exmpl_run():
    qc = add_4bit_num()
    print("4-bit adder:")
    print(qc.draw("text"))

if __name__ == "__main__":
    exmpl_run()