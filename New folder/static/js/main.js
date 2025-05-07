let circuit = [];
let numQubits = 4;
let histogramChart = null;

function initializeCircuit() {
    const qubitArea = document.getElementById('qubit-area');
    qubitArea.innerHTML = '';
    
    for (let i = 0; i < numQubits; i++) {
        const line = createQubitLine(i);
        qubitArea.appendChild(line);
    }
    
    document.getElementById('qubit-count').textContent = numQubits;
}

function createQubitLine(index) {
    const line = document.createElement('div');
    line.className = 'qubit-line';
    
    const label = document.createElement('div');
    label.className = 'qubit-label';
    label.textContent = `q${index}`;
    line.appendChild(label);
    
    const wire = document.createElement('div');
    wire.className = 'qubit-wire';
    line.appendChild(wire);
    
    const cells = document.createElement('div');
    cells.className = 'cell-container';
    
    for (let j = 0; j < 8; j++) {
        const cell = document.createElement('div');
        cell.className = 'circuit-cell';
        cell.dataset.qubit = index;
        cell.dataset.position = j;
        
        cell.addEventListener('dragover', e => {
            e.preventDefault();
            cell.classList.add('dragover');
        });
        
        cell.addEventListener('dragleave', () => {
            cell.classList.remove('dragover');
        });
        
        cell.addEventListener('drop', handleGateDrop);
        
        cells.appendChild(cell);
    }
    
    line.appendChild(cells);
    return line;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    initializeCircuit();
    setupGateListeners();
    
    document.getElementById('add-qubit').addEventListener('click', addQubit);
    document.getElementById('remove-qubit').addEventListener('click', removeQubit);
    document.getElementById('clear-circuit').addEventListener('click', clearCircuit);
    document.getElementById('run-circuit').addEventListener('click', runSimulation);
});

function setupGateListeners() {
    document.querySelectorAll('.gate').forEach(gate => {
        gate.draggable = true;
        gate.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('gate', gate.dataset.gate);
        });
    });
}

function handleGateDrop(e) {
    e.preventDefault();
    const cell = e.currentTarget;
    cell.classList.remove('dragover');
    
    if (cell.children.length > 0) return;
    
    const gateType = e.dataTransfer.getData('gate');
    const qubit = parseInt(cell.dataset.qubit);
    const position = parseInt(cell.dataset.position);
    
    placeGate(gateType, qubit, position, cell);
}

function restoreCircuitState() {
    circuit.forEach(gate => {
        const cell = document.querySelector(
            `.circuit-cell[data-qubit="${gate.qubit}"][data-position="${gate.position}"]`
        );
        if (cell) {
            placeGate(gate.type, gate.qubit, gate.position, cell);
        }
    });
}

function placeGate(gateType, qubit, position, cell) {
    const gate = document.createElement('div');
    gate.className = `gate-placed ${gateType}`;
    gate.textContent = gateType.toUpperCase();
    
    const deleteBtn = document.createElement('div');
    deleteBtn.className = 'delete-gate';
    deleteBtn.textContent = '×';
    deleteBtn.onclick = (e) => {
        e.stopPropagation();
        cell.innerHTML = '';
        removeGateFromCircuit(qubit, position);
    };
    
    gate.appendChild(deleteBtn);
    cell.appendChild(gate);
    
    circuit.push({ type: gateType, qubit, position });
    updateCircuitStats();
}

function clearCircuit() {
    circuit = [];
    const qubitArea = document.getElementById('qubit-area');
    // Clear all placed gates
    document.querySelectorAll('.gate-placed').forEach(gate => gate.remove());
    // Clear histogram
    if (histogramChart) {
        histogramChart.destroy();
        histogramChart = null;
    }
    // Reset statistics
    document.getElementById('circuit-depth').textContent = '0';
    document.getElementById('total-gates').textContent = '0';
}

function addQubit() {
    if (numQubits < 8) {
        numQubits++;
        // Don't copy existing circuit state when adding new qubit
        initializeCircuit();
        document.getElementById('qubit-count').textContent = numQubits;
    }
}

function runSimulation() {
    if (circuit.length === 0) {
        alert('Please add gates to the circuit before running simulation');
        return;
    }

    // Sort circuit by position to ensure correct gate order
    const sortedCircuit = circuit.sort((a, b) => a.position - b.position);

    fetch('/simulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            circuit: sortedCircuit,
            num_qubits: numQubits
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateHistogram(data);
        } else {
            alert('Simulation error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Simulation error:', error);
        alert('Failed to run simulation. Please try again.');
    });
}

function downloadCircuit() {
    const data = {
        circuit,
        num_qubits: numQubits
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'quantum_circuit.json';
    a.click();
    URL.revokeObjectURL(url);
}

function updateQubitCount() {
    document.getElementById('qubit-count').textContent = numQubits;
}

function updateHistogram(data) {
    const ctx = document.getElementById('measurement-histogram').getContext('2d');
    
    if (histogramChart) {
        histogramChart.destroy();
    }
    
    const labels = Object.keys(data.counts).sort();
    const values = labels.map(label => data.counts[label]);
    const total = values.reduce((sum, val) => sum + val, 0);
    
    histogramChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'State Probability',
                data: values.map(v => (v / total).toFixed(3)),
                backgroundColor: 'rgba(25, 118, 210, 0.5)',
                borderColor: 'rgba(25, 118, 210, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    title: {
                        display: true,
                        text: 'Probability'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Quantum States'
                    }
                }
            }
        }
    });

    // Update statistics
    document.getElementById('circuit-depth').textContent = data.circuit_depth;
    document.getElementById('total-gates').textContent = circuit.length;
}

function updateCircuitStats() {
    document.getElementById('total-gates').textContent = circuit.length;
    document.getElementById('circuit-depth').textContent = Math.max(...circuit.map(gate => gate.position), 0);
}
