# Remove in future: currently allows us to import qnetdes
import sys
sys.path.insert(0, '/Users/zacespinosa/Foundry/qnetdes')

from qnetdes import *
from pyquil import Program
from pyquil.gates import *
from pyquil.api import WavefunctionSimulator

# wf_sim = WavefunctionSimulator()
# def getWaveFunction(p): 
#     waveFunction = wf_sim.wavefunction(p)
#     probs = waveFunction.get_outcome_probs()
#     print(probs)
    
class Alice(Agent): 
    def teleport(self, phi, a): 
        # Entangle Ancilla and Phi
        self.program += CNOT(phi, a)
        self.program += H(phi)

        # Measure Ancilla and Phi
        phi_measured = MEASURE(phi, ro[0])
        a_measured = MEASURE(a, ro[1])
    
        # Send Cbits
        bits = [phi_measured, a_measured]
        self.csend('bob', bits)

    def run(self): 
        # Define Alice's Qubits
        a = self.qubits[0]
        phi = self.qubits[1]
        self.teleport(phi,a)        


class Bob(Agent): 
    def run(self):
        b = self.qubits[0]
        phi_measured, a_measured = self.crecv('alice')
        if phi_measured: self.program += Z(b)
        if a_measured: self.program += X(b)
        
        b_measured =  MEASURE(b, ro[2]) 
        print(b_measured)

p = Program(H(0), CNOT(0,1), H(2))
ro = p.declare('ro', 'BIT', 3)
alice = Alice(p, [0, 2], 'alice')
bob = Bob(p, [1], 'bob')

QConnect(alice, bob, [None])
CConnect(alice, bob)
Simulation(alice, bob, p).run()