from flask import Flask, render_template, jsonify, request
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
from qiskit.quantum_info import Operator
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json
        circuit = data.get('circuit', [])
        num_qubits = data.get('num_qubits', 4)
        
        if not circuit:
            return jsonify({
                'success': False,
                'error': 'Empty circuit'
            })

        qc = QuantumCircuit(num_qubits, num_qubits)
        
        # Process gates in order
        for gate in circuit:
            gate_type = gate['type']
            qubit = gate['qubit']
            
            if qubit >= num_qubits:
                continue  # Skip invalid qubit indices
                
            try:
                if gate_type == 'h':
                    qc.h(qubit)
                elif gate_type == 'x':
                    qc.x(qubit)
                elif gate_type == 'y':
                    qc.y(qubit)
                elif gate_type == 'z':
                    qc.z(qubit)
                elif gate_type == 'cnot':
                    control = gate.get('control', max(0, qubit - 1))
                    if control != qubit and control < num_qubits:
                        qc.cx(control, qubit)
                elif gate_type == 'swap':
                    target = gate.get('target', min(num_qubits - 1, qubit + 1))
                    if target != qubit and target < num_qubits:
                        qc.swap(qubit, target)
            except Exception as e:
                print(f"Error applying gate {gate_type}: {str(e)}")
                continue
        
        qc.measure_all()
        
        # Execute circuit
        simulator = AerSimulator()
        job = simulator.run(qc, shots=1000)
        result = job.result()
        counts = result.get_counts(qc)
        
        # Ensure all possible states are represented
        all_states = [format(i, f'0{num_qubits}b') for i in range(2**num_qubits)]
        complete_counts = {state: counts.get(state, 0) for state in all_states}
        
        return jsonify({
            'counts': complete_counts,
            'circuit_depth': qc.depth(),
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
