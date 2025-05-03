import numpy as np

class QuantumSimulator:
    def __init__(self, num_qubits=1):
        self.num_qubits = num_qubits
        self.initialize_state(num_qubits)
    
    def initialize_state(self, num_qubits):
        self.qubits = np.zeros(2**num_qubits, dtype=complex)
        self.qubits[0] = 1.0
    
    def apply_gate(self, gate, target_qubit, control_qubit=None):
        if gate == 'H':  # Hadamard gate
            had = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
            self._apply_single_qubit_gate(had, target_qubit)
        elif gate == 'X':  # NOT/X gate
            x_gate = np.array([[0, 1], [1, 0]])
            if control_qubit is not None:
                self._apply_controlled_gate(x_gate, control_qubit, target_qubit)
            else:
                self._apply_single_qubit_gate(x_gate, target_qubit)
        elif gate == 'Z':  # Z gate
            z_gate = np.array([[1, 0], [0, -1]])
            if control_qubit is not None:
                self._apply_controlled_gate(z_gate, control_qubit, target_qubit)
            else:
                self._apply_single_qubit_gate(z_gate, target_qubit)
    
    def _apply_single_qubit_gate(self, gate_matrix, target_qubit):
        new_state = np.zeros_like(self.qubits)
        for i in range(len(self.qubits)):
            bit = (i >> target_qubit) & 1
            new_i = i ^ (1 << target_qubit)
            new_state[i] += gate_matrix[0][bit] * self.qubits[i]
            new_state[new_i] += gate_matrix[1][bit] * self.qubits[i]
        self.qubits = new_state
    
    def _apply_controlled_gate(self, gate_matrix, control_qubit, target_qubit):
        new_state = np.zeros_like(self.qubits)
        for i in range(len(self.qubits)):
            control_val = (i >> control_qubit) & 1
            if control_val:
                target_val = (i >> target_qubit) & 1
                new_i = i ^ (1 << target_qubit)
                new_state[i] += gate_matrix[0][target_val] * self.qubits[i]
                new_state[new_i] += gate_matrix[1][target_val] * self.qubits[i]
            else:
                new_state[i] = self.qubits[i]
        self.qubits = new_state
    
    def measure(self, qubit=None):
        if qubit is None:
            probabilities = np.abs(self.qubits) ** 2
            return np.random.choice(len(self.qubits), p=probabilities)
        else:
            result = 0
            prob_one = 0
            for i in range(len(self.qubits)):
                if (i >> qubit) & 1:
                    prob_one += abs(self.qubits[i])**2
            if np.random.random() < prob_one:
                result = 1
            return result
    
    def get_probabilities(self):
        return np.abs(self.qubits) ** 2
    
    def print_state(self):
        state_str = ""
        for i, amp in enumerate(self.qubits):
            if abs(amp) > 1e-10:
                state = format(i, f'0{self.num_qubits}b')
                state_str += f"{amp:.3f}|{state}⟩ + "
        return state_str[:-3] if state_str else "0"
    
    def run_circuit(self, circuit_data):
        self.initialize_state(circuit_data['num_qubits'])
        for operation in circuit_data['operations']:
            control = operation.get('control_qubit', None)
            self.apply_gate(operation['gate'], operation['target'], control)
        return {'measurement': int(self.measure())}