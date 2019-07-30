import sys
sys.path.insert(0, '/Users/zacespinosa/Foundry/qnetdes')
sys.path.insert(1, '/Users/matthewradzihovsky/documents/qnetdes')

from pyquil import Program
from pyquil.api import WavefunctionSimulator, QVMConnection
from pyquil.gates import *
from qnetdes import *

__all__ = ["cat_entangler", "cat_disentangler"]#, "non_local_CNOT"]

def distributed_gate(agent):
    agent.using_distributed_gate = not agent.using_distributed_gate

def cat_entangler(control, measure, targets, caller, entangled=False):
    '''
    Performs the cat entangler, one of two primitive operations for 
    distributed quantum computing which can be used to implement non-local operations.
    Projects the state Alice's local control bit (phi) on entangled qubits owned by other Agents, 
    allowing Agents to effectively use Alice's qubit as a control for their own operations.
    e.g non-local CNOTs, non-local controlled gates, and teleportation. 

    :param (Agent, Integer, Classical Register): Agent owning phi, phi, and register to store measurement
    :param Integer measure: qubit to be measured
    :param List<Integer> targets: qubits from other Agents
    :param Agent caller: agent calling function
    :param Boolean entangled: true if qubits from other Agents are already maximally entangled
    '''
    phi, ro = control
    p = caller.program
    agents = [measure] + targets

    # Tell Tracer to Ignore Operations
    distributed_gate(caller)

    # If qubits are not already entangled, and distribute all non-control qubits
    if not entangled:
        p += H(measure)
        for i in range(len(agents) - 1):
            qubits1= agents[i] 
            qubits2= agents[i+1]
            p += CNOT(qubits1, qubits2)
    
    # Project control qubit onto qubit and measure
    p += CNOT(phi, measure)
    p += MEASURE(measure, ro[measure]) 
    
    # Conditionally Perform Measure Operations 
    for qubit in agents:
        p.if_then(ro[measure], X(qubit))

    # Tell Tracer We're Done
    distributed_gate(caller)

def cat_disentangler(control, targets, caller):
    '''
    Performs the cat disentangler, second of two primitive operations for 
    distributed quantum computing which can be used to implement non-local operations.
    Restores all qubits to state before cat_entangler was performed.

    :param (Integer, Classical Register): Agent owning phi, phi, and register to store measurement
    :param List<Integer> targets: qubits from other Agents
    :param Agent caller: agent calling function
    '''
    phi, ro = control
    p = caller.program

    # Tell Tracer to Ignore Operations
    distributed_gate(caller)

    # Perform Hadamard of each qubit
    for q in targets: p += H(q)
    # Measure target bits and execut Bit-Flip to restore to 0
    for t in targets: 
        p += MEASURE(t, ro[t])
        p.if_then(ro[t], X(t))

    # Perform XOR between all measured bits and if true perform Z rotation on phi.
    # This will restore the original state of phi
    for i in range(len(targets) - 1, 0, -1):
        p += XOR(ro[targets[i-1]], ro[targets[i]])

    p.if_then(ro[targets[0]], Z(phi))

    # Tell Tracer We're Done
    distributed_gate(caller)


    