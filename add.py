from qiskit import QuantumCircuit

def carry(qc, cin, a, b, cout):
    qc.ccx(a, b, cout)
    qc.cx(a, b)
    qc.ccx(cin, b, cout)

def carry_dg(qc, cin, a, b, cout):
    qc.ccx(cin, b, cout)
    qc.cx(a, b)
    qc.ccx(a, b, cout)

def sum_gate(qc, cin, a, b):
    qc.cx(a, b)
    qc.cx(cin, b)

def add_4bit_num():
    qc = QuantumCircuit(12)
    a = [0, 1, 2, 3]
    b = [4, 5, 6, 7]
    cout = 8
    helper = [9, 10, 11]
    carries = helper + [cout]  
    qc.ccx(a[0], b[0], carries[0])
    carry(qc, carries[0], a[1], b[1], carries[1])
    carry(qc, carries[1], a[2], b[2], carries[2])
    carry(qc, carries[2], a[3], b[3], carries[3])
    qc.cx(a[3], b[3])
    sum_gate(qc, carries[2], a[3], b[3])
    carry_dg(qc, carries[1], a[2], b[2], carries[2])
    sum_gate(qc, carries[1], a[2], b[2])
    carry_dg(qc, carries[0], a[1], b[1], carries[1])
    sum_gate(qc, carries[0], a[1], b[1])
    qc.ccx(a[0], b[0], carries[0])
    qc.cx(a[0], b[0])
    return qc

def exmpl_run():
    qc = add_4bit_num()
    print("4-bit adder:")
    print(qc.draw("text"))

if __name__ == "__main__":
    exmpl_run()
