.. _distributed-protocol: 

=========================================================
Distributed Quantum Protocol
=========================================================

Due to a variety of constraints, modern quantum computers
are often limited to working with a small set of qubits and therefore limited to solving small problems involving few qubits. 
Distributed quantum computing (DQC) is a means of leveraging the computation power of a quantum network 
in order to solve a problem too large for any single quantum computer. Each 
node on a quantum network is connected via a classical and quantum channel and managers its own
classical register for storing bits of information such as qubit measurements. Nodes may not
modify or interact with qubits that they do not manage without physically receiving the qubits
from a different node, performing teleportation, or via non-local operations.

In this demo we introduce netQuil's distributed protocol library that implements a set of
non-local operations commonly used in DQC. Specifically, this library will introduce the 
primitive cat-entangler and cat-disentangler as introduced by Yimsiriwattana and Lomonaco, 
and their usage in non-local CNOTs, non-local controlled gates, and teleportation. 

Cat-Entangler
=============
The cat-entangler allows a single agent (Alice) in posession of a control qubit (phi)
to distribute control over multiple agents (Bob and Charlie), given that Alice, Bob, and Charlie
share a system of three entangled qubits that can be placed in a cat-like state.

Protocol
--------

.. image:: ../img/cat-entangler.png

The dark curved lines between wires two and four represent entangled qubits 
(i.e. :math:`\frac{1}{\sqrt{2}}(|000\rangle + |111\rangle)`). In this case, wires one and two
are owned by Alice, three by Bob, and four by Charlie. The double-lines represent a
measurement result, that is passed via a classical channel and used to control the X gates.  

Usage
-----
netQuils implementation of the cat entangler requires that only one agent to initiate and execute the circuit.
netQuil will transport the qubits between agents, update either clocks, and appropriately apply noise.
If `notify=True` the cat entangler will send a classical bit to each participating agent (excluding the caller), notifying
all parties that the entangler has finished. If `entangler=False` the cat_entangler will entangle
the target qubits and the measurement qubit (i.e. a is the measurement qubit in the example) before performing the circuit. 

.. code-block:: python
    :linenos:

    class Alice(Agent): 
        def run(self):
            # Define Qubits
            a, phi = self.qubits 
            b = bob.qubits[0]
            
            cat_entangler(
                control=(self, phi, a, ro),
                targets=[(bob, b)],
                entangled=False,
                notify=True
            )

    class Bob(Agent): 
        def run(self):
            # Measurement from cat entangler
            self.crecv(alice.name)
            # Notification that cat entangler is complete
            self.crecv(alice.name)
    
    # In this example we omit the following...
    # 1. Define Ro and Qubits
    # 2. Instantiate Agents
    # 3. Connect Agents
    # 4. Run Simulation

Cat-Disentangler
================
Once all agents have used the shared control bit to perform their local operation the
cat-disentangler can be used to restore the system to its former state.

Protocol
--------

.. image:: ../img/cat-disentangler.png

The Z gate on the first wire is controlled by the exclusive-or (:math:`\oplus`) of the classical bits
resulting from the measurements on qubits two and three.   

Usage
-----

.. code-block:: python
    :linenos:

    class Alice(Agent): 
        '''
        Alice uses cat-entangler to perform distributed quantum teleportation
        '''
        def run(self):
            a, phi = self.qubits 
            b = bob.qubits[0]

            cat_disentangler(
                control=(self, phi, ro),
                targets=[(bob, b)],
                notify=True
            )

    class Bob(Agent):
        def run(self): 
            # Wait for cat-disentangler to finish
            self.crecv(alice.name)
            # ... Perform operations with teleported state
            b = bob.qubits[0]

Non-local CNOT and Teleportation
================================
Cat-entangler and cat-disentangler are primitive circuits that can be used 
to contruct non-local CNOT gates, non-local controlled gates and teleportation. 
In fact, the controlled-NOT gate plus all one-qubit unitary gates is a universal set. Therefore, 
in order to contruct a universal set of operators for DQC, we must only contruct a 
non-local CNOT gate, which can be done with the cat-entangler and cat-disentangler. 

Protocol
--------

.. image:: ../img/non-local-cnot.png

.. image:: ../img/teleportation.png

The swap gate in the teleportation circuit is only necessary in order to fully restore 
the third qubit to its original state. 

Example
-------
Here is an example of teleportation using the cat-entangler and cat-disentangler. 

.. code-block:: python
    :linenos: 

    import sys
    sys.path.insert(0, '/Users/zacespinosa/Foundry/netQuil')
    sys.path.insert(1, '/Users/matthewradzihovsky/documents/netQuil')

    from pyquil import Program
    from pyquil.api import WavefunctionSimulator, QVMConnection
    from pyquil.gates import *
    from netQuil import *

    class Alice(Agent): 
        def teleportation(self, phi, a, b):
            cat_entangler(
                control=(self, phi, a, ro),
                targets=[(bob, b)],
                entangled=False,
                notify=False
            )
            cat_disentangler(
                control=(bob, b, ro),
                targets=[(self, phi)],
                notify=False
            )

        def run(self):
            # Define Qubits
            a, phi = self.qubits 
            b = bob.qubits[0]

            # Teleport
            self.teleportation(phi, a, b)

    class Bob(Agent): 
        def run(self):
            # Receive Measurement from Cat-entangler
            self.crecv(alice.name)

    p = Program()

    # Prepare psi
    p += H(2)
    p += RZ(1.2, 2)

    # Create Classical Memory
    ro = p.declare('ro', 'BIT', 3)

    alice = Alice(p, qubits=[0,2], name='alice')
    bob = Bob(p, qubits=[1], name='bob')

    QConnect(alice, bob)
    CConnect(alice, bob)

    Simulation(alice, bob).run()
    qvm = QVMConnection()
    qvm.run(p)

Source Code
-----------
The source code for the cat-entangler can be found `here <https://github.com/att-innovate/netQuil>`_. Contributions are encouraged! 
To learn more about distributed quantum computing and the cat-like state checkout
`this <https://arxiv.org/abs/quant-ph/0402148>`_ paper by Yimsiriwattana and Lomonaco.

