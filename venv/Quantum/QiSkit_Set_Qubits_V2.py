from qiskit import *
import matplotlib.pyplot as plt
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
import networkx as nx

#==================================================================================
#      This algorithm runs set amounts of qubits in groups (Improved attempt)
#==================================================================================

# Changeable variables
nodes = 20 # How many nodes the graph has
mUseBits = 10 # How many bits the program can use

graphMatrix = [[0 for i in range(nodes)] for j in range(nodes)] # defines matrix

for x in range(nodes): # For the easy ability to print the Matrix
    for y in range(nodes):
        graphMatrix[x][y] = 0
        print(graphMatrix[x][y], end = " ")
    print()

bitsUsed = int(((nodes * nodes) - nodes) / 2) # This is where the nodes are checked to the matrix
simulator = Aer.get_backend('qasm_simulator') # Simulator/quantum computer used

qr = QuantumRegister(mUseBits) # Creates a mBit quantum register
cr = ClassicalRegister(mUseBits) # Creates a mBit classical register
circuit = QuantumCircuit(qr, cr) # Creating a Quantum Circuit from qr and cr

listOfBits = [] # Where the random numbers are stored

print("Full bit runs required:", int(bitsUsed / mUseBits))
print("Remainders required:", int(bitsUsed % mUseBits), "\n")

def GenerateRandom(length): # This generates the random numbers for each register of qubits
    if length == 0:
        return
    print(f'    [Length of Register]: {length}')
    for i in range(length):
        circuit.h(qr[i])
    circuit.measure(qr, cr) # Measure the quantum register
    job = execute(circuit, simulator, shots = 1)
    job_monitor(job)
    counts = job.result().get_counts()
    print("[New Random Numbers added]: ", end = " ")
    for i in range(length):
        print(int(str(counts)[i + 2]), end = " ")
        listOfBits.append(int(str(counts)[i + 2]))
    print("\n")

for i in range(int(bitsUsed / mUseBits)): # Full qubit runs
    GenerateRandom(mUseBits)
GenerateRandom(int(bitsUsed % mUseBits)) # Partial qubits run

print("[All Random Numbers Created]:", listOfBits)
print()
counter = 0

#==================================================================================
#                  This is mostly for the graphics and things
#==================================================================================

F = nx.Graph()

for i in range(nodes): #Adds nodes
    F.add_node(i)

for i in range(nodes):
    for j in range(i):
        #graphMatrix[i][j] = listOfBits[counter] #To make an undirected graph
        graphMatrix[j][i] = listOfBits[counter]
        if listOfBits[counter] == 1:
            F.add_edge(i, j)
        counter = counter + 1

for x in range(nodes): #Easy Matrix print
    for y in range(nodes):
        print(graphMatrix[x][y], end = " ")
    print()

plt.figure()

pos = nx.spring_layout(F)

labels = nx.get_edge_attributes(F,'weight')
nx.draw(F, pos, with_labels = True)
nx.draw_networkx_edge_labels(F, pos, edge_labels = labels)
plt.show()