# Remove in future: currently allows us to import netQuil
import sys
sys.path.insert(0, '/Users/zacespinosa/Foundry/netQuil')
sys.path.insert(1, '/Users/matthewradzihovsky/documents/netQuil')

from pyquil import Program
from pyquil.api import WavefunctionSimulator, QVMConnection
from pyquil.gates import *
from netQuil import *

####################################################
# TRIALS
####################################################

# class Alice(Agent):
#     def run(self):
#         p = self.program
#         for q in self.qubits:
#             p += H(q)
#             p += X(q)
#             self.qsend('Bob', [q])

# class Bob(Agent):
#     def run(self):
#         p = self.program
#         for _ in range(3): 
#             q = self.qrecv(alice.name)[0]
#             p += MEASURE(q, ro[q])

# p = Program()
# ro = p.declare('ro', 'BIT', 3)

# alice = Alice(p, qubits=[0,1,2])
# bob = Bob(p)

# QConnect(alice, bob)
# Simulation(alice, bob).run(10, [Alice, Bob])

# print(p)
# qvm = QVMConnection()
# results = qvm.run(p)
# print(results)

####################################################
# TRIALS WITH DEVICES 
####################################################

class Alice(Agent):
    def run(self):
        p = self.program
        for q in self.qubits:
            p += H(q)
            p += X(q)
            self.qsend('Bob', [q])

class Bob(Agent):
    def run(self):
        p = self.program
        for _ in range(1): 
            q = self.qrecv(alice.name)[0]
            p += MEASURE(q, ro[q])

p = Program()
ro = p.declare('ro', 'BIT', 3)

laser = Laser(rotation_prob_variance=.9) 
alice = Alice(p, qubits=[0])
bob = Bob(p)

# Declare devices
fiber = Fiber(length=10, attenuation_coefficient=-.20)
QConnect(alice, bob, transit_devices=[fiber])

Simulation(alice, bob).run(trials=5, agent_classes=[Alice, Bob]) 

# print(p)
qvm = QVMConnection()
results = qvm.run(p)
print(results)
