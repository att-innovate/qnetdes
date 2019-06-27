# Remove in future: currently allows us to import qnetdes
import sys
sys.path.insert(0, '/Users/zacespinosa/Foundry/qnetdes')

from qnetdes import *
from pyquil import Program
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator, QVMConnection

def waveFunction(p):
    wf_sim = WavefunctionSimulator()
    waveFunction = wf_sim.wavefunction(p)
    print(waveFunction)
    
class Alice(Agent): 
    def run(self): 
        # Define Alice's qubits
        a, phi = self.qubits
        p = self.program
        # Entangle Ancilla and Phi
        p += CNOT(phi, a)
        p += H(phi)

        # Measure Ancilla and Phi
        p += MEASURE(phi, ro[0])
        p += MEASURE(a, ro[1])
    
        # Send Cbits
        bits = [0,1]
        self.csend('bob', bits)

class Bob(Agent): 
    def run(self):
        b = self.qubits[0]
        self.crecv('alice')

        p = self.program
        p.if_then(ro[1], X(b))
        p.if_then(ro[0], Z(b))

        waveFunction(p)
        qvm = QVMConnection()
        result = qvm.run(p)

# Create Phi
p = Program(H(2))
waveFunction(p)
# Entangle qubits 0 and 1. 
p += Program(H(0))
p += CNOT(0,1) 

# Create Classical Memory
ro = p.declare('ro', 'BIT', 3)

# Create Alice and Bob. Give Alice qubit 0 (ancilla) and qubit 2 (phi). Give Bob qubit 1
alice = Alice(p, [0, 2], [], 'alice')
bob = Bob(p, [1], [], 'bob')

# Connect Alice and Bob via a quantum connection and classical connection with no transit devices
QConnect(alice, bob, transit_devices=[None])
CConnect(alice, bob)

# Run simulation
Simulation(alice, bob).run()

# wf_sim = WavefunctionSimulator()
# waveFunction = wf_sim.wavefunction(p)