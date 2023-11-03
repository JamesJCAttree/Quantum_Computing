from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from qiskit.tools import job_monitor
from numpy import pi

#==================================================================================
#                 This was the original attempt at BB84 algorithm
#==================================================================================

# Changeable variables
qubits = 10 # int(input("Qubits #: "))

def RandomNumber(numbers): # This returns a list of random numbers for the users to use later -------------------------------------------------- RNG
    qr = QuantumRegister(numbers * 2)
    cr = ClassicalRegister(numbers * 2)
    circuit = QuantumCircuit(qr, cr)
    for i in range(numbers * 2):
        circuit.h(qr[i]) # Apply Hadamard gate to each qubit
        circuit.measure(qr[i], cr[i])  # Measure each qubit while in loop
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=1)
    job_monitor(job)
    counts = job.result().get_counts()
    return [int(str(counts)[int(i + 2)]) for i in range(numbers * 2)]

randomList = RandomNumber(qubits)

qr = QuantumRegister(qubits * 2) # Creates registers
cr = ClassicalRegister(qubits * 2)
circuit = QuantumCircuit(qr, cr)

for i in range(qubits):# Bob's Qubits ---------------------------------------------------------------------------------------------------- Bob's Qubits
    #This is where the bases are
    if randomList[i] == 0:
        print('0', end = " ")
        circuit.h(qr[i])  # Apply Hadamard gate to each qubit
        circuit.measure(qr[i], cr[i])  # Measure each qubit while in loop
    else:
        print('1', end = " ")
        circuit.u(pi / 2, pi / 2, pi / 2, qr[i])  # Apply U gate to each qubit
        circuit.measure(qr[i], cr[i])  # Measure each qubit while in loop
print()
for i in range(qubits): # Alice's Qubits
    #This is where the bases are
    if randomList[i + qubits] == 0:
        print('0', end = " ")
        circuit.h(qr[i + qubits])  # Apply Hadamard gate to each qubit
        circuit.measure(qr[i + qubits], cr[i + qubits])  # Measure each qubit while in loop
    else:
        print('1', end = " ")
        circuit.u(pi / 2, pi / 2, pi / 2, qr[i + qubits])  # Apply U gate to each qubit
        circuit.measure(qr[i + qubits], cr[i + qubits])  # Measure each qubit while in loop

circuit.measure(qr, cr) # Measurement of Qubits
circuit.draw()
# print(circuit) # For the ciruit to be drawn
simulator = Aer.get_backend('qasm_simulator') # Simulator code
job = execute(circuit, simulator, shots=1)
job_monitor(job)
counts = job.result().get_counts()

listOfBits = [int(str(counts)[int(i + 2)]) for i in range(qubits * 2)]
for i in range(qubits * 2): # Check qubits to each other
    if qubits == i:
        print()
    if i == 0:
        print("[B]:", end = " ")
    if i == qubits:
        print("[A]:", end = " ")
    print(listOfBits[i], end = " ")
counter = 0 # To caculate percentage
print("\n[T]:", end = " ")
for i in range(qubits): # Gives percentage of simularity
    if listOfBits[i] == listOfBits[i + qubits]:
        counter += 1
        print("1", end = " ")
    else:
        print(" ", end = " ")
print("\nPercent:", (counter / qubits) * 100, "%\nMiddle man: ", end = "")
if (counter / qubits) * 100 >= 40 and (counter / qubits) * 100 <= 60:
    print("False")
else:
    print("Possible")

l1 = [] # 0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1
message = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1] # You gotta do math on this if you do the XOR gate after, because it changes the percentages
print("[M]", message, "\n[B]", listOfBits)



for i in range(qubits * 2): # This runs the combonation between the two quantum decryption
    print("[T]: [", listOfBits[i], "| ", message[i], "]") # stop confusing myself
    if listOfBits[i] == 0 and message[i] == 1:
        l1.append(0)
    elif listOfBits[i] == 1 and message[i] == 1:
        l1.append(1)
    elif listOfBits[i] == 0 and message[i] == 0:
        l1.append(int(RandomNumber(1)[0]))
    elif listOfBits[i] == 1 and message[i] == 0:
        l1.append(int(RandomNumber(1)[0]))
print("[L]", l1)

#for i in range(len(l1)):
#    if i == (int)(len(l1) / 2):
#        print()
#    print(l1[i], end = " ")
