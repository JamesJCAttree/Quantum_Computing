from qiskit import *
import matplotlib.pyplot as plt
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
import networkx as nx
from numpy import pi

#==================================================================================
#         This proves a random entanglement number generator (No graphing)
#==================================================================================

# Changeable variable
nodes = 5

#defines matrix
graphMatrix = [[0 for i in range(nodes)] for j in range(nodes)]

for x in range(nodes): #Easy Matrix print
    for y in range(nodes):
        graphMatrix[x][y] = 0
        print(graphMatrix[x][y], end = " ")
    print()

#This is where the nodes are checked to the matrix
bitsUsed = int(((nodes * nodes) - nodes) / 2)

simulator = Aer.get_backend('qasm_simulator') #Cool kids simulator

qr = QuantumRegister(bitsUsed) #Creates a two bit quantum register
cr = ClassicalRegister(bitsUsed) #Creates a two bit classical register

# Creating a Quantum Circuit from qr and cr

circuit = QuantumCircuit(qr, cr)

print("Q Reg", qr)

def Entanglement_1():
    for i in range(bitsUsed):
        circuit.h(qr[i])

    for i in range(int(bitsUsed/2)):
        circuit.ry(pi / 10, qr[i])

def Entanglement_2():
    for i in range(bitsUsed):
        circuit.h(qr[i])

    for i in range(int(bitsUsed/2)):
        circuit.ry(pi / 2, qr[i])

Entanglement_2() # Run the code for the entanglement choosen

circuit.draw(output='mpl')
plt.show()

circuit.measure(qr, cr) #Measure the quantum register

job = execute(circuit, simulator, shots=1)
                               
print('Executing Job...\n')                 
job_monitor(job)
counts = job.result().get_counts()

listOfBits = []

for i  in range(bitsUsed):
    listOfBits.append(int(str(counts)[int(i + 2)]))

print(listOfBits)

print()
counter = 0