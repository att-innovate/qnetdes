import sys
sys.path.insert(0, '/Users/zacespinosa/Foundry/qnetdes')
sys.path.insert(1, '/Users/matthewradzihovsky/documents/qnetdes')

from pyquil import Program
from pyquil.api import WavefunctionSimulator, QVMConnection
from pyquil.gates import *
from qnetdes import *

__all__ = ["cat_entangler", "cat_disentangler"]

def distributed_gate(agent):
    agent.using_distributed_gate = not agent.using_distributed_gate

def cat_entangler(control, measure, targets, entangled=False):
    '''
    Performs the cat entangler, one of two primitive operations for 
    distributed quantum computing which can be used to implement non-local operations.
    Projects the state Alice's local control bit (phi) on entangled qubits owned by other Agents, 
    allowing Agents to effectively use Alice's qubit as a control for their own operations.
    e.g non-local CNOTs, non-local controlled gates, and teleportation. 

    :param (agent, int, classical register): Agent owning phi, phi, and register to store measurement
    :param (agent, qubit) measure: qubit to be measured and agent owning qubit
    :param List<(agent, qubit)> targets: agent and agent's qubit that will be altered
    :param Boolean entangled: true if qubits from other Agents are already maximally entangled
    '''
    phi, ro = control
    measure_qubit, measure_agent = measure 
    p = measure_agent.program

    # Collect all qubits except control bit
    qubits = [measure_qubit] + [q[1] for q in targets]

    # Tell Tracer to Ignore Operations
    distributed_gate(measure_agent)

    # If qubits are not already entangled, and distribute all non-control qubits
    if not entangled:
        p += H(measure)
        for i in range(len(qubits) - 1):
            q1 = qubits[i] 
            q2 = qubits[i+1]
            p += CNOT(q1, q2)
    
    # Project control qubit onto qubit and measure
    p += CNOT(phi, measure)
    p += MEASURE(measure, ro[measure]) 

    # Send result of qubit that has been measured to all other agents
    cbit = [1] # Hard code a placeholder value until ro is calculated
    for agent in [t[0] for t in targets]:
        measure_agent.csend(agent.name, cbit)
        agent.crecv(measure_agent.name)

    # Conditionally Perform Measure Operations 
    for q in qubits:
        p.if_then(ro[measure], X(q))

    # Tell Tracer We're Done
    distributed_gate(measure_agent)

def cat_disentangler(control, targets):
    '''
    Performs the cat disentangler, second of two primitive operations for 
    distributed quantum computing which can be used to implement non-local operations.
    Restores all qubits to state before cat_entangler was performed.

    :param (agent, int, classical register): 
    :param List<(agent, qubit)> targets: agent and agent's qubit that will be altered
    '''
    agent, phi, ro = control
    p = agent.program

    # Tell Tracer to Ignore Operations
    distributed_gate(agent)

    # Perform Hadamard of each qubit
    for _, q in targets: p += H(q)

    # Measure target bits and execute bit-flip to restore to 0
    for a, q in targets: 
        p += MEASURE(q, ro[q])
        p.if_then(ro[q], X(q))

        # Send qubit measurement to owner of phi in order to perform XOR
        cbit = [1] # Hard code a placeholder value until ro[q] is calculated
        a.csend(agent, cbit)
        agent.crecv(a.name)

    # Perform XOR between all measured bits and if true perform Z rotation on phi.
    # This will restore its original state
    for i in range(len(targets) - 1, 0, -1):
        p += XOR(ro[targets[i-1][1]], ro[targets[i][1]])

    p.if_then(ro[targets[0][1]], Z(phi))

    # Tell Tracer We're Done
    distributed_gate(agent)


    