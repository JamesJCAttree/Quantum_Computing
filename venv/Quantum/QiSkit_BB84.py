from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from qiskit.tools import job_monitor
from qiskit.circuit.library import XGate
import matplotlib
from qiskit.visualization import circuit_drawer

#==================================================================================
#                  This is my implementation of the BB84 Algorithm
#==================================================================================

# Changeable variables
silence = True
aliceMessage = "1011101011" # The message Alice want to send unga bunga
blockSize = 4
eve = True

bobFullMeasure = []
quantumStates = []
aliceBase = []
bobBase = []
qState = []
bobMeasure = []

eveFullMeasure = []
eveMeasure = []
eveBase = []

qrHolder = QuantumRegister(blockSize)
crHolder = ClassicalRegister(blockSize)
circuitHolder = QuantumCircuit(qrHolder, crHolder)

def RandomNumber(numbers, measure): # This returns a list of random numbers for the users to use later -------------------------------------------------- RNG
    qr = QuantumRegister(numbers * 2)
    cr = ClassicalRegister(numbers * 2)
    circuit = QuantumCircuit(qr, cr)
    for i in range(numbers * 2):
        circuit.h(qr[i]) # Apply Hadamard gate to each qubit
        if measure == True:
            circuit.measure(qr[i], cr[i]) # Measure each qubit while in loop
    if measure == True:
        simulator = Aer.get_backend('qasm_simulator') # Remove measurement for later use wit h Alice
        job = execute(circuit, simulator, shots = 1)
        job_monitor(job, quiet = silence)
        counts = job.result().get_counts()
        return [int(str(counts)[int(i + 2)]) for i in range(numbers * 2)]
    return circuit

def SetToQuantum(baseBit, msgBit, location):
    print("\t[Currently testing]: [", baseBit, "&", msgBit, "] For:", location) # Fix this 1 is rotated
    qreg_q = QuantumRegister(1, 'q')
    creg_c = ClassicalRegister(1, 'c')
    circuit = QuantumCircuit(qreg_q, creg_c)
    if baseBit == 0 and msgBit == 1: # Check this
        circuit.reset(qreg_q[0])
        circuit.x(qreg_q)
        circuitHolder.append(circuit, [qrHolder[location]], [crHolder[0]])
        print(circuit)
        return circuitHolder
    elif baseBit == 1 and msgBit == 1: # Check this
        circuit.reset(qreg_q[0])
        circuit.x(qreg_q[0])
        circuit.h(qreg_q[0])
        circuitHolder.append(circuit, [qrHolder[location]], [crHolder[0]])
        print(circuit)
        return circuitHolder
    elif baseBit == 0 and msgBit == 0:
        circuit.reset(qreg_q[0])
        circuitHolder.append(circuit, [qrHolder[location]], [crHolder[0]])
        print(circuit)
        return circuit # This is a zero in a quantum state, so use a zero gate
    elif baseBit == 1 and msgBit == 0:
        circuit.reset(qreg_q[0])
        circuit.h(qreg_q[0])
        circuitHolder.append(circuit, [qrHolder[location]], [crHolder[0]])
        print(circuit)
        return circuit # This is a quantum Negate a zero gate

def AliceLocation(pos):
    qState = []
    print("[Alice's Message]:", int(aliceMessage[pos])) # Prints the message
    aliceBase.append(int(RandomNumber(1, True)[0])) # Create and print Alice's base
    print("\n[Alice's base]:", aliceBase)
    qState.append(SetToQuantum(aliceBase[pos], int(aliceMessage[pos]), pos)) # Create the quantum state of Alice's base & Alice's message
    print("\n[Quantum State]:", qState) # Print the Alice quantum bit
    quantumStates.append(qState)

def Loading(percent):
    count = 0
    print("[", end = "")
    for i in range(20):
        if count <= percent:
            print("□", end = "")
            count += 0.05
        else:
            print(" ", end = "")
    print("]")
            
# Start protocol here -------------------------------------------------------------------------------------------

k = int(len(aliceMessage)/blockSize) + 1
t = k

while (not(k <= 1 and (1 + (t - k) * blockSize > len(aliceMessage)))): # I think this has to be negated
    i = (t - k) * blockSize
    j = 0
    while i + j < len(aliceMessage) and j < blockSize:
        AliceLocation(j)
        print(i + j, ":", len(aliceMessage), "|")
        Loading((i + j) / len(aliceMessage))
        print("List Location: ", j, " + ", i, " = ", j + i) # This means j + i = block location then the block
        j = j + 1

    if eve: # This is Eve interfering
        for x in range(j): # This is Bob's part right here -----------------------------------------------------------
            eveBase.append(int(RandomNumber(1, True)[0]))
            print(len(bobBase), "| [Eve's Base]", eveBase)
            temp = x
            if eveBase[temp] == 1: # This H measures the qubit for later
                circuitHolder.h(qrHolder[temp]) # H Measure

        circuitHolder.measure(qrHolder, crHolder) # This is the process of measuring the bits then adding them to a list
        simulator = Aer.get_backend('qasm_simulator')
        job = execute(circuitHolder, simulator, shots = 1024)
        result = job.result()
        counts = result.get_counts()
        counts_list = []
        for key, value in counts.items():
            counts_list.append((key, value))
        eveMeasure = counts_list[0][0]
        eveMeasure = eveMeasure[::-1]
        eveFullMeasure.append(eveMeasure)

        print(f"\n\t[Block #{int(i / blockSize) + 1} Circuit]\n")
        print(circuitHolder)

        qrHolder = QuantumRegister(blockSize) # This resets the qubits
        crHolder = ClassicalRegister(blockSize)
        circuitHolder = QuantumCircuit(qrHolder, crHolder)

        AliceLocation(x) # Reset Alice's message quantum state

    for x in range(j): # This is Bob's part right here -----------------------------------------------------------
        bobBase.append(int(RandomNumber(1, True)[0]))
        print(len(bobBase), "| [Bob's Base]", bobBase)
        temp = x
        if bobBase[temp] == 1: # This H measures the qubit for later
            circuitHolder.h(qrHolder[temp]) # H Measure


    circuitHolder.measure(qrHolder, crHolder) # This is the process of measuring the bits then adding them to a list
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuitHolder, simulator, shots = 1024)
    result = job.result()
    counts = result.get_counts()
    counts_list = []
    for key, value in counts.items():
        counts_list.append((key, value))
    bobMeasure = counts_list[0][0]
    bobMeasure = bobMeasure[::-1]
    bobFullMeasure.append(bobMeasure)

    print(f"\n\t[Block #{int(i / blockSize) + 1} Circuit]\n")
    print(circuitHolder)

    qrHolder = QuantumRegister(blockSize) # This resets the qubits
    crHolder = ClassicalRegister(blockSize)
    circuitHolder = QuantumCircuit(qrHolder, crHolder)

    k = k - 1

print("\n[Blocks]") # This prints them in blocks
for i in range(len(aliceMessage)):
    if i % blockSize == 0:
        print()
        print("\t[Block:", int(i / blockSize) + 1,"]")
    print(quantumStates[i])

tempBlockCounter = 0

for i in range(len(aliceMessage)):
    if(i % blockSize == 0 and i != 0):
        tempBlockCounter = int(i / blockSize)
    bobMeasure = bobMeasure + bobFullMeasure[tempBlockCounter][i - (blockSize * tempBlockCounter):i - (blockSize * tempBlockCounter) + 1]
    if(eve):
        eveMeasure = eveMeasure + eveFullMeasure[tempBlockCounter][i - (blockSize * tempBlockCounter):i - (blockSize * tempBlockCounter) + 1]

print("[Alice MSG]:", aliceMessage, "| [Bob MES]:", bobMeasure[0:len(aliceMessage)], "| [Eve MES]:"  if eve else "", eveMeasure[0:len(aliceMessage)] if eve else "") # Print the list of measurement results
print("[A]:", aliceBase, " | [B]:", bobBase)

count = 0
for i in range(len(aliceMessage)):
    if aliceMessage[i] == bobMeasure[i]:
        count = count + 1

print("[Similarity]:", int((count / len(aliceMessage)) * 100), "%")
print()