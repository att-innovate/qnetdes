import sys
sys.path.insert(0, '/Users/matthewradzihovsky/documents/qnetdes')
sys.path.insert(1, '/Users/matthewradzihovsky/documents/qnetdes')

import numpy as np
import uuid

from qnetdes import *
from pyquil.gates import *
from pyquil.quil import DefGate

__all__ = ["bit_flip", "phase_flip", "depolarizing_channel", "measure","normal_unitary_rotation"]

ro_declared = False

def bit_flip(program, qubit, prob: float):
    '''
    Apply a bit flip with probability

    :param Program program: program to apply noise to
    :param Integer qubit: qubit to apply noise to 
    :param Float prob: probability of apply noise 
    '''
    #define the gates
    noisy_I = np.asarray([[1, 0], [0, 1]])
    noisy_X = np.asarray([[0, 1], [1, 0]])

    #get the Quil definition for the new gate
    noisy_I_definition = DefGate("flip_NOISY_I", noisy_I)
    noisy_X_definition = DefGate("flip_NOISY_X", noisy_X)

    #get the gate constructor
    flip_NOISY_I = noisy_I_definition.get_constructor()
    flip_NOISY_X = noisy_X_definition.get_constructor()
    program += noisy_I_definition
    program += noisy_X_definition
    
    #apply
    if np.random.rand() > prob:
        program += flip_NOISY_X(qubit)
    else:
        program += flip_NOISY_I(qubit)
    

def phase_flip(program, qubit, prob: float):
    '''
    Apply a phase flip with probability

    :param Program program: program to apply noise to
    :param Integer qubit: qubit to apply noise to 
    :param Float prob: probability of apply noise 
    '''
    #define the gates
    noisy_I = np.asarray([[1, 0], [0, 1]])
    noisy_Z = np.asarray([[1, 0], [0, -1]])

    #get the Quil definition for the new gate
    noisy_I_definition = DefGate("phase_NOISY_I", noisy_I)
    noisy_Z_definition = DefGate("phase_NOISY_Z", noisy_Z)

    #get the gate constructor
    phase_NOISY_I = noisy_I_definition.get_constructor()
    phase_NOISY_Z = noisy_Z_definition.get_constructor()
    program += noisy_I_definition
    program += noisy_Z_definition
    
    #apply
    if np.random.rand() > prob:
        program += phase_NOISY_Z(qubit)
    else:
        program += phase_NOISY_I(qubit)

def depolarizing_channel(program, qubit, prob: float):
    '''
    Apply depolarizing noise with probability

    :param Program program: program to apply noise to
    :param Integer qubit: qubit to apply noise to 
    :param Float prob: probability of apply noise 
    '''
    #define the gates
    noisy_I = np.asarray([[1, 0], [0, 1]])
    noisy_X = np.asarray([[1, 0], [0, -1]])
    noisy_Z = np.asarray([[1, 0], [0, -1]])
    noisy_Y = np.asarray([[0, 0-1.0j], [0+1.0j, 0]])

    #get the Quil definition for the new gate
    noisy_I_definition = DefGate("dp_NOISY_I", noisy_I)
    noisy_X_definition = DefGate("dp_NOISY_X", noisy_X)
    noisy_Z_definition = DefGate("dp_NOISY_Z", noisy_Z)
    noisy_Y_definition = DefGate("dp_NOISY_Y", noisy_Y)

    #get the gate constructor
    dp_NOISY_I = noisy_I_definition.get_constructor()
    dp_NOISY_X = noisy_X_definition.get_constructor()
    dp_NOISY_Z = noisy_Z_definition.get_constructor()
    dp_NOISY_Y = noisy_Y_definition.get_constructor()
    program += (noisy_I_definition, noisy_X_definition, noisy_Z_definition, noisy_Y_definition)
    
    random_gate = random.randint(1,3)
    #apply
    if np.random.rand() < prob:
        program += NOISY_I(qubit)
    elif random_gate == 1:
        program += NOISY_X(qubit)
    elif random_gate == 2:
        program += NOISY_Y(qubit)
    elif random_gate == 3:
        program += NOISY_Z(qubit)

def measure(program, qubit, prob: float, name="ro"):
    '''
    Measure the qubit with probability

    :param Program program: program to apply noise to
    :param Integer qubit: qubit to apply noise to 
    :param Float prob: probability of apply noise 
    '''
    if np.random.rand()> prob:
        global ro_declared
        for inst in program.instructions:
            try:
                if inst.name == "ro":
                    ro_declared = True
            except:
                pass

        if ro_declared:
            ro = program.declare("a"+str(uuid.uuid1().int), 'BIT', 1)
        else:
            ro = program.declare("ro", 'BIT', 1)
            ro_declared = True
            program += MEASURE(qubit, ro)



def normal_unitary_rotation(program, qubit, prob:float):
    '''
    Apply X and Z rotation with probability

    :param Program program: program to apply noise to
    :param Integer qubit: qubit to apply noise to 
    :param Float prob: probability of apply noise 
    '''
    if np.random.rand() > prob:
        x_angle, z_angle = np.random.normal(0,self.variance,2)
        program += RX(x_angle, qubit)
        program += RZ(z_angle, qubit)
    