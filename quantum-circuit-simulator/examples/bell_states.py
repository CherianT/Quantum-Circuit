"""
Bell state preparation circuit
This creates a maximally entangled state |Φ+⟩ = (|00⟩ + |11⟩)/√2
"""
from simulator import QuantumSimulator

# Create simulator with 2 qubits
qsim = QuantumSimulator(2)

# Apply Hadamard gate to the first qubit
qsim.apply_gate('H', 0)

# Apply CNOT (controlled-X) gate with control=0, target=1
qsim.apply_gate('X', 1, control_qubit=0)

# Print the final state
print("Bell state preparation:")
print(qsim.print_state())

# Get measurement probabilities
probs = qsim.get_probabilities()
for i, p in enumerate(probs):
    if p > 0.01:  # Only show non-zero probabilities
        state = format(i, f'0{qsim.num_qubits}b')
        print(f"|{state}⟩: {p:.4f}")