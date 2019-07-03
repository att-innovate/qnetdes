import sys
sys.path.insert(0, '/Users/matthewradzihovsky/documents/qnetdes')
sys.path.insert(1, '/Users/matthewradzihovsky/documents/qnetdes')

import numpy as np
import uuid

from pyquil import Program
from pyquil.gates import *
from qnetdes import *

__all__ = ["Fiber"]

class Device(): 
    def __init__(self): 
        pass
    
    def apply(self, program, qubits):
        pass

class Fiber(Device):
    def __init__(self, length, attenuation_coefficient = -0.16, apply_error=True):

        decibel_loss = length*attenuation_coefficient
        self.attenuation = 10 ** (decibel_loss / 10)
        self.apply_error = apply_error
        self.length = length

        
    def apply(self, program, qubits):
        for qubit in qubits:
            if 1 > self.attenuation and qubit is not None:
                print('using this device', 'fiber' + str(uuid.uuid1().int))
                identifier = np.random.randint(1,10000)
                ro = program.declare('fiber' + str(uuid.uuid1().int), 'BIT', 1)
                program += MEASURE(qubit, ro) 
        delay = self.length
        return delay

        

    