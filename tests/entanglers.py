import sys
sys.path.insert(0, '/Users/zacespinosa/Foundry/qnetdes')
sys.path.insert(1, '/Users/matthewradzihovsky/documents/qnetdes')

from pyquil import Program
from pyquil.api import WavefunctionSimulator, QVMConnection
from pyquil.gates import *
from qnetdes import *

def printWF(p):
    '''
    Prints the wavefunction from simulating a program p
    '''
    wf_sim = WavefunctionSimulator()
    waveFunction = wf_sim.wavefunction(p)
    print(waveFunction)

class Charlie(Agent):
    def run(self):

class Alice(Agent): 
    def run(self):
        p = self.program

        # Define Qubits
        phi = self.qubits[0]
        qubitsCharlie = self.qrecv(charlie.name)
        a = qubitsCharlie[0]
        b = 1

        # Use cat-entangler
        cat_entangler(
            control=(phi, ro),
            measure=a,
            targets=[b],
            caller=self,
            entangled=True
        ) 

class Bob(Agent): 
    def run(self):
        p = self.program
        # Define Qubits
        qubitsCharlie = self.qrecv(charlie.name)
        b = qubitsCharlie[0]
        phi = alice.qubits[1]

        # Use cat_disentangler
        cat_disentangler(
            control=(b, ro),
            targets=[phi],
            caller=self,
        )

p = Program()

# Prepare 5 qubit entangled system
p += H(0)
p += CNOT(0,1)
p += CNOT(0,2)
p += CNOT(0,3)
p += CNOT(0,5)

# Prepare psi 
p += RZ(1.2, 6)
p += Z(6)
printWF(p)

# Create Classical Memory
ro = p.declare('ro', 'BIT', 5)

# Create Alice, Bob, and Charlie. Give Alice qubit 2 (phi). Give Charlie qubits [0,1] (Bell State Pairs). 
alice = Alice(p, qubits=[0,6], name='alice')
bob = Bob(p, qubits=[1], name='bob')
charlie = Charlie(p, qubits=[2], name='charlie')
don = Don(p, qubits=[])
eve = 


# Connect agents to distribute qubits and report results
QConnect(alice, charlie)
QConnect(bob, charlie)
QConnect(alice, bob)
CConnect(alice, bob)

Simulation(alice, bob, charlie).run()
qvm = QVMConnection()
qvm.run(p)
printWF(p)