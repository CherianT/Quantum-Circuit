"""
Grover's search algorithm for 2 qubits
This demonstrates quantum amplitude amplification to find a marked item
"""
from simulator import QuantumSimulator

# Create simulator with 2 qubits
qsim = QuantumSimulator(2)

# Step 1: Create superposition using Hadamard gates
for i in range(2):
    qsim.apply_gate('H', i)

print("After initialization with Hadamard gates:")
print(qsim.print_state())

# Step 2: Oracle - mark the state |01⟩
# We can implement this with a controlled-Z gate with control=0, target=1,
# preceded and followed by X gates on qubit 0 to flip the control condition
qsim.apply_gate('X', 0)  # Flip control qubit
qsim.apply_gate('Z', 1, control_qubit=0)  # Controlled-Z
qsim.apply_gate('X', 0)  # Flip back

print("After Oracle (marking |01⟩):")
print(qsim.print_state())

# Step 3: Diffusion operator (Grover's diffusion)
# Apply H gates to all qubits
for i in range(2):
    qsim.apply_gate('H', i)

# Apply Z gates to all qubits
for i in range(2):
    qsim.apply_gate('Z', i)

# Apply controlled-Z with control=0, target=1
qsim.apply_gate('Z', 1, control_qubit=0)

# Apply H gates to all qubits again
for i in range(2):
    qsim.apply_gate('H', i)

print("After diffusion operator:")
print(qsim.print_state())

# Measure both qubits
result0 = qsim.measure(0)
result1 = qsim.measure(1)
print(f"Measurement results: {result0}{result1}")