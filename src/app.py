from flask import Flask, render_template, request, jsonify
from simulator import QuantumSimulator

app = Flask(__name__)
simulator = QuantumSimulator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    circuit_data = request.json
    result = simulator.run_circuit(circuit_data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)