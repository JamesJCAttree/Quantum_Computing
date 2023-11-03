from qiskit import *
import matplotlib.pyplot as plt
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
import networkx as nx

#==================================================================================
#                  This algorithm runs all qubits at once (First Attempt)
#==================================================================================

# Changeable variables
nodes = 5 # How many nodes the graph has
mUseBits = 3 # How many bits the program can use

graphMatrix = [[0 for i in range(nodes)] for j in range(nodes)] # defines matrix

for x in range(nodes):
    for y in range(nodes):
        graphMatrix[x][y] = 0
        print(graphMatrix[x][y], end = " ")
    print()

# This is where the nodes are checked to the matrix
bitsUsed = int(((nodes * nodes) - nodes) / 2)

simulator = Aer.get_backend('qasm_simulator')  # Cool kids simulator

qr = QuantumRegister(mUseBits)  # Creates an mBit quantum register
cr = ClassicalRegister(mUseBits)  # Creates an mBit classical register

# Creating a Quantum Circuit from qr and cr
circuit = QuantumCircuit(qr, cr)

print("Q Reg", qr)

listOfBits = []

print("Full bit runs required:", int(bitsUsed / mUseBits))
print("Remainders required:", int(bitsUsed % mUseBits))
runs = 0
testing = 0

for i in range(min(mUseBits, bitsUsed)):
    #print("\nRuns:", i)
    runs = runs + 1
    circuit.h(qr[i])
    circuit.measure(qr[i], cr[i])
    job = execute(circuit, simulator, shots=1)
    print('Executing Job...\n')
    job_monitor(job)
    counts = job.result().get_counts()
    circuit.draw()
    for i in range(mUseBits):
        #print(i, " : ", mUseBits)
        #print(int(str(counts)[int(i + 2)]), end=" ")
        listOfBits.append(int(str(counts)[int(i + 2)]))

for i in range(int(bitsUsed % mUseBits)):  # Modded remainder
    runs = runs + 1
    circuit.h(qr[i])
    circuit.measure(qr[i], cr[i])
    job = execute(circuit, simulator, shots=1)
    print('Executing Job...\n')
    job_monitor(job)
    counts = job.result().get_counts()
    circuit.draw()
    print(int(str(counts)[int(3)]), end=" ")
    listOfBits.append(int(str(counts)[int(3)]))
print()
print(listOfBits)
print("Correct Amount: ", end="")
if len(listOfBits) == int(((nodes * nodes) - nodes) / 2):
    print(True)
print("Program runs: ", runs)

print()
counter = 0

# ==================================================================================
#                  This is mostly for the graphics and things
# ==================================================================================

F = nx.Graph()

for i in range(nodes):  # Adds nodes
    F.add_node(i)

for i in range(nodes):
    for j in range(i):
        if counter < len(listOfBits):
            graphMatrix[j][i] = listOfBits[counter]  # To make an undirected graph
            if listOfBits[counter] == 1:
                F.add_edge(i, j)
            counter = counter + 1

for x in range(nodes): #Easy Matrix print
    for y in range(nodes):
        print(graphMatrix[x][y], end = " ")
    print()

print("Number of edges:", listOfBits.count(1), "| Percent: ", (int)((listOfBits.count(1) / len(listOfBits)) * 100), "%")
print("Number of non-edges:", listOfBits.count(0), "| Percent: ", (int)((listOfBits.count(0) / len(listOfBits))  * 100), "%")

plt.figure()

pos = nx.spring_layout(F)

labels = nx.get_edge_attributes(F,'weight')
nx.draw(F, pos, with_labels = True)
nx.draw_networkx_edge_labels(F, pos, edge_labels = labels)
plt.show()