"""
Quantum Teleportation Circuit
This demonstrates how to teleport a quantum state from one qubit to another
"""
from simulator import QuantumSimulator
import numpy as np

# Create simulator with 3 qubits
# qubit 0: the qubit with state to be teleported
# qubit 1 and 2: entangled qubits shared between sender and receiver
qsim = QuantumSimulator(3)

# Step 1: Prepare the state to teleport on qubit 0
# Let's create a superposition state
qsim.apply_gate('H', 0)
