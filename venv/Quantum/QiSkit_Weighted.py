from qiskit import *
import matplotlib.pyplot as plt
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
import networkx as nx
from numpy import pi

#==================================================================================
#          This algorithm creates a weighted random graph (Uses all bits)
#==================================================================================

# Changeable variables
nodes = 9
prob = pi / 0.3 # This is a RY Gate input here (see "QiSkit_Quantum_Rotation" for examples)

graphMatrix = [[0 for i in range(nodes)] for j in range(nodes)] # defines matrix
listOfBits = []

for x in range(nodes): # Easy Matrix set & print
    for y in range(nodes):
        graphMatrix[x][y] = 0
        print(graphMatrix[x][y], end = " ")
    print()

bitsUsed = int(((nodes * nodes) - nodes) / 2) # This is where the nodes are checked to the matrix

simulator = Aer.get_backend('qasm_simulator') # Setting the quantum computer/simulator

qr = QuantumRegister(bitsUsed) # Creates a bitsUsed length quantum register
cr = ClassicalRegister(bitsUsed) # Creates a bitsUsed length classical register
circuit = QuantumCircuit(qr, cr) # Creating a Quantum Circuit from qr and cr

for i in range(bitsUsed): # Rotates the qubit
    circuit.ry(prob, qr[i])
circuit.measure(qr, cr) # Sets the measurement gates in the quantum register

job = execute(circuit, simulator, shots = 1) # Simulates the circuit
print('Executing Job...\n')                 
job_monitor(job)
counts = job.result().get_counts()
circuit.draw() # Draws the circuit

for i  in range(bitsUsed):
    listOfBits.append(int(str(counts)[int(i + 2)]))

print(listOfBits)
print()

#==================================================================================
#                  This is mostly for the graphics and things
#==================================================================================

counter = 0
F = nx.Graph()

for i in range(nodes): #Adds nodes
    F.add_node(i)

for i in range(nodes):
    for j in range(i):
        graphMatrix[j][i] = listOfBits[counter]
        if listOfBits[counter] == 1:
            F.add_edge(i, j)
        counter = counter + 1

for x in range(nodes): # Easy Matrix print
    for y in range(nodes):
        print(graphMatrix[x][y], end = " ")
    print()

plt.figure()
pos = nx.spring_layout(F)
labels = nx.get_edge_attributes(F,'weight')
nx.draw(F, pos, with_labels = True)
nx.draw_networkx_edge_labels(F, pos, edge_labels = labels)
plt.show()