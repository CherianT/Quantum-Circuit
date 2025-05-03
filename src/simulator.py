import numpy as np

class QuantumSimulator:
    def __init__(self):
        self.qubits = None
    
    def initialize_state(self, num_qubits):
        self.qubits = np.zeros(2**num_qubits, dtype=complex)
        self.qubits[0] = 1.0
    
    def apply_gate(self, gate, target_qubit):
        # Basic implementation for single-qubit gates
        if gate == 'H':  # Hadamard gate
            had = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
            self._apply_single_qubit_gate(had, target_qubit)
    
    def _apply_single_qubit_gate(self, gate_matrix, target_qubit):
        num_qubits = int(np.log2(len(self.qubits)))
        new_state = np.zeros_like(self.qubits)
        
        for i in range(len(self.qubits)):
            bit = (i >> target_qubit) & 1
            new_i = i ^ (1 << target_qubit)
            
            new_state[i] += gate_matrix[0][bit] * self.qubits[i]
            new_state[new_i] += gate_matrix[1][bit] * self.qubits[i]
        
        self.qubits = new_state
    
    def measure(self):
        probabilities = np.abs(self.qubits) ** 2
        return np.random.choice(len(self.qubits), p=probabilities)
    
    def run_circuit(self, circuit_data):
        self.initialize_state(circuit_data['num_qubits'])
        for operation in circuit_data['operations']:
            self.apply_gate(operation['gate'], operation['target'])
        return {'measurement': int(self.measure())}