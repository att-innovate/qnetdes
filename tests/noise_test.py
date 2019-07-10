import sys
sys.path.insert(1, '/Users/matthewradzihovsky/documents/qnetdes')
sys.path.insert(0, '/Users/zacespinosa/Foundry/qnetdes')

from pyquil import Program
from pyquil.api import WavefunctionSimulator, QVMConnection
from pyquil.gates import *
from qnetdes import *

class Bob(Agent):
   
    def run(self):
        p = self.program
        print("In Bob")
        noise.bit_flip(p,0,0)
        print("bit flip")
        printWF(p)
        p += H(0)
        print("Haddamard")
        printWF(p)
        noise.phase_flip(p,0,0)
        print("phase flip")
        printWF(p)
        noise.measure(p,0,0)
        print("measure")
        printWF(p)
    
def printWF(program):
        wf_sim = WavefunctionSimulator()
        waveFunction = wf_sim.wavefunction(program)
        print(waveFunction)
    

qvm = QVMConnection()
program = Program()

#define agents
bob = Bob(program, qubits=[0,2])

#connect agents

#simulate agents
Simulation(bob).run()
results = qvm.run(program, trials=1)

#print initial states

print('Bob\'s results:', results)

print('Bob\'s time:', bob.time)
for inst in program.instructions:
    try:
        if inst.name == "ro":
            print("done")
    except:
        pass
        
    


