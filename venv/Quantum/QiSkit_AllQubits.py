from qiskit import *
import matplotlib.pyplot as plt
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
import networkx as nx

#==================================================================================
#                  This algorithm runs all qubits at once
#==================================================================================

# Changeable variable
nodes = 15 # Define number of nodes

graphMatrix = [[0 for i in range(nodes)] for j in range(nodes)] # Create graph matrix

bitsUsed = int(((nodes * nodes) - nodes) / 2) # Create edges between nodes based on quantum circuit result

qr = QuantumRegister(bitsUsed) # Quantum circuit information
cr = ClassicalRegister(bitsUsed)
circuit = QuantumCircuit(qr, cr)

for i in range(bitsUsed): # Setting up the circuit via gates and measurement
    circuit.h(qr[i])
circuit.measure(qr, cr)

simulator = Aer.get_backend('qasm_simulator') # Simulating qubits
job = execute(circuit, simulator, shots=1)
job_monitor(job)
counts = job.result().get_counts()
listOfBits = [int(str(counts)[int(i + 2)]) for i in range(bitsUsed)]

F = nx.Graph() # Create graph from matrix and edges
for i in range(nodes):
    F.add_node(i)

#==================================================================================
#                  This is mostly for the graphics and things
#==================================================================================

counter = 0
for i in range(nodes):
    for j in range(i):
        graphMatrix[j][i] = listOfBits[counter]
        if listOfBits[counter] == 1:
            F.add_edge(i, j)
        counter += 1

for x in range(nodes):
    for y in range(nodes):
        print(graphMatrix[x][y], end=" ")
    print()

print("Number of edges:", listOfBits.count(1), "| Percent: ", (int)((listOfBits.count(1) / len(listOfBits)) * 100), "%")
print("Number of non-edges:", listOfBits.count(0), "| Percent: ", (int)((listOfBits.count(0) / len(listOfBits))  * 100), "%")

plt.figure() # Draw graph
pos = nx.spring_layout(F)
labels = nx.get_edge_attributes(F,'weight')
nx.draw(F, pos, with_labels=True)
nx.draw_networkx_edge_labels(F, pos, edge_labels=labels)
plt.show()