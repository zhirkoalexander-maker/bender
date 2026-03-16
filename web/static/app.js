// APP STATE
const state = {
    currentShape: 'triangle',
    currentColor: '#FF6B6B',
    points: [],
    shapes: [],
    history: [],
    gridEnabled: true,
    snapEnabled: true,
    animationsEnabled: false,
    selectedShape: null,
};

// CANVAS SETUP
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const rect = canvas.getBoundingClientRect();

// CONSTANTS
const GRID_SIZE = 20;
const POINT_SIZE = 8;
const SNAP_DISTANCE = 10;

// ============= INITIALIZATION =============
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    setDefaultActiveShape();
    redraw();
});

// ============= EVENT LISTENERS =============
function setupEventListeners() {
    // Shape buttons
    document.querySelectorAll('.shape-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            state.currentShape = btn.dataset.shape;
            state.points = [];
            resetUI();
            updateUI();
            redraw();
        });
    });

    // Color buttons
    document.querySelectorAll('.color-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            state.currentColor = btn.dataset.color;
            document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            updateColorDisplay();
        });
    });

    // Tools
    document.getElementById('rotate-btn').addEventListener('click', showRotateDialog);
    document.getElementById('scale-btn').addEventListener('click', showScaleDialog);
    document.getElementById('mirror-h-btn').addEventListener('click', () => mirrorShape('horizontal'));
    document.getElementById('mirror-v-btn').addEventListener('click', () => mirrorShape('vertical'));
    document.getElementById('move-btn').addEventListener('click', showMoveDialog);
    document.getElementById('clear-btn').addEventListener('click', clearAll);

    // Quick actions
    document.getElementById('undo-btn').addEventListener('click', undo);
    document.getElementById('finish-btn').addEventListener('click', finishShape);
    document.getElementById('save-btn').addEventListener('click', saveDrawing);

    // Toggles
    document.getElementById('grid-toggle').addEventListener('change', (e) => {
        state.gridEnabled = e.target.checked;
        redraw();
    });

    document.getElementById('snap-toggle').addEventListener('change', (e) => {
        state.snapEnabled = e.target.checked;
    });

    document.getElementById('animate-toggle').addEventListener('change', (e) => {
        state.animationsEnabled = e.target.checked;
    });

    // Canvas events
    canvas.addEventListener('click', onCanvasClick);
    canvas.addEventListener('dblclick', finishShape);
    canvas.addEventListener('mousemove', onCanvasMouseMove);
    canvas.addEventListener('mouseout', () => {
        updateCoordinates(0, 0);
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'z' || e.key === 'Z') undo();
        if (e.key === 'f' || e.key === 'F') finishShape();
        if (e.key === 'q' || e.key === 'Q') clearAll();
    });

    // Modal
    document.getElementById('modal-ok').addEventListener('click', handleModalOk);
    document.getElementById('modal-cancel').addEventListener('click', hideModal);
    document.getElementById('modal-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleModalOk();
    });
}

// ============= CANVAS DRAWING =============
function onCanvasClick(e) {
    const rect = canvas.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;

    // Apply snap to grid
    if (state.snapEnabled) {
        x = Math.round(x / GRID_SIZE) * GRID_SIZE;
        y = Math.round(y / GRID_SIZE) * GRID_SIZE;
    }

    // Add point
    state.points.push([x, y]);
    addHistory(`Added point ${state.points.length}`);

    // Auto-complete shapes
    if (state.currentShape === 'square' && state.points.length === 2) {
        createSquare();
        finishShape();
    } else if (state.currentShape === 'rectangle' && state.points.length === 2) {
        createRectangle();
        finishShape();
    } else if (state.currentShape === 'circle' && state.points.length === 2) {
        finishShape();
    } else if (state.currentShape === 'triangle' && state.points.length === 3) {
        analyzeShape();
    }

    updateUI();
    redraw();
}

function onCanvasMouseMove(e) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    updateCoordinates(x, y);
}

function updateCoordinates(x, y) {
    document.getElementById('coords').textContent = `X: ${Math.round(x)}, Y: ${Math.round(y)}`;
}

// ============= DRAWING FUNCTIONS =============
function redraw() {
    // Clear canvas
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw grid
    if (state.gridEnabled) {
        drawGrid();
    }

    // Draw all saved shapes
    state.shapes.forEach((shape, idx) => {
        drawShape(shape.points, shape.color, false, idx === state.selectedShape);
    });

    // Draw current shape
    if (state.points.length > 0) {
        drawCurrentShape();
    }
}

function drawGrid() {
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 1;

    for (let i = 0; i < canvas.width; i += GRID_SIZE) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvas.height);
        ctx.stroke();
    }

    for (let i = 0; i < canvas.height; i += GRID_SIZE) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
    }
}

function drawCurrentShape() {
    const points = state.points;

    // Draw lines
    ctx.strokeStyle = state.currentColor;
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    if (state.currentShape === 'circle' && points.length >= 1) {
        const [cx, cy] = points[0];
        if (points.length >= 2) {
            const [px, py] = points[1];
            const radius = Math.hypot(px - cx, py - cy);
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.stroke();
            ctx.fillStyle = state.currentColor + '30';
            ctx.fill();
        }
        // Center marker
        ctx.fillStyle = '#FF00FF';
        ctx.fillRect(cx - 4, cy - 4, 8, 8);
    } else {
        // Draw lines between points
        for (let i = 0; i < points.length - 1; i++) {
            ctx.beginPath();
            ctx.moveTo(points[i][0], points[i][1]);
            ctx.lineTo(points[i + 1][0], points[i + 1][1]);
            ctx.stroke();
        }
    }

    // Draw points
    points.forEach((point, idx) => {
        drawPoint(point[0], point[1], idx + 1);
    });
}

function drawShape(points, color, dashed = false, selected = false) {
    if (points.length < 2) return;

    ctx.strokeStyle = selected ? '#FFD700' : color;
    ctx.lineWidth = selected ? 4 : 3;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    if (dashed) {
        ctx.setLineDash([5, 5]);
    }

    // Draw closed shape
    for (let i = 0; i < points.length; i++) {
        const p1 = points[i];
        const p2 = points[(i + 1) % points.length];
        ctx.beginPath();
        ctx.moveTo(p1[0], p1[1]);
        ctx.lineTo(p2[0], p2[1]);
        ctx.stroke();
    }

    ctx.setLineDash([]);

    // Fill if finished
    if (points.length >= 3) {
        ctx.fillStyle = color + '20';
        ctx.beginPath();
        ctx.moveTo(points[0][0], points[0][1]);
        for (let i = 1; i < points.length; i++) {
            ctx.lineTo(points[i][0], points[i][1]);
        }
        ctx.closePath();
        ctx.fill();
    }
}

function drawPoint(x, y, label = '') {
    ctx.fillStyle = '#FFFF00';
    ctx.strokeStyle = '#000000';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(x, y, POINT_SIZE, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    if (label) {
        ctx.fillStyle = '#000000';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, x, y);
    }
}

// ============= SHAPE CREATION =============
function createSquare() {
    if (state.points.length < 2) return;
    const [x1, y1] = state.points[0];
    const [x2, y2] = state.points[1];
    const side = Math.hypot(x2 - x1, y2 - y1);
    const dx = (x2 - x1) / side;
    const dy = (y2 - y1) / side;
    const px = -dy;
    const py = dx;

    state.points = [
        [x1, y1],
        [x1 + dx * side, y1 + dy * side],
        [x1 + dx * side + px * side, y1 + dy * side + py * side],
        [x1 + px * side, y1 + py * side]
    ];
}

function createRectangle() {
    if (state.points.length < 2) return;
    const [x1, y1] = state.points[0];
    const [x2, y2] = state.points[1];
    state.points = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]];
}

// ============= TRANSFORMATIONS =============
function analyzeShape() {
    if (state.points.length < 2) return;

    const sides = [];
    for (let i = 0; i < state.points.length; i++) {
        const p1 = state.points[i];
        const p2 = state.points[(i + 1) % state.points.length];
        const dist = Math.hypot(p2[0] - p1[0], p2[1] - p1[1]);
        sides.push(dist);
    }

    const perimeter = sides.reduce((a, b) => a + b, 0);

    // Shoelace formula for area
    let area = 0;
    for (let i = 0; i < state.points.length; i++) {
        const p1 = state.points[i];
        const p2 = state.points[(i + 1) % state.points.length];
        area += p1[0] * p2[1] - p2[0] * p1[1];
    }
    area = Math.abs(area) / 2;

    const n = state.points.length;
    let shapeType = 'Polygon';
    
    if (n === 3) shapeType = 'Triangle';
    else if (n === 4) shapeType = 'Quadrilateral';

    document.getElementById('shape-name').textContent = `Shape: ${shapeType}`;
    document.getElementById('shape-stats').textContent = `Vertices: ${n} | Perimeter: ${perimeter.toFixed(1)}px | Area: ${area.toFixed(1)}px²`;
    document.getElementById('shape-formula').textContent = `Sides: ${sides.map(s => s.toFixed(0)).join(', ')}`;

    updateStatus(`Analyzed: ${shapeType}`);
}

async function rotateShape(angle) {
    if (state.points.length < 2) {
        alert('Draw a shape first!');
        return;
    }

    try {
        const response = await fetch('/api/rotate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ points: state.points, angle: angle })
        });
        const data = await response.json();
        state.points = data.points;
        addHistory(`Rotated ${angle}°`);
        redraw();
    } catch (error) {
        console.error('Rotation error:', error);
    }
}

async function scaleShape(factor) {
    if (state.points.length < 2) {
        alert('Draw a shape first!');
        return;
    }

    try {
        const response = await fetch('/api/scale', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ points: state.points, factor: factor })
        });
        const data = await response.json();
        state.points = data.points;
        addHistory(`Scaled ${factor}x`);
        redraw();
    } catch (error) {
        console.error('Scale error:', error);
    }
}

async function mirrorShape(axis) {
    if (state.points.length < 2) {
        alert('Draw a shape first!');
        return;
    }

    try {
        const response = await fetch('/api/mirror', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ points: state.points, axis: axis })
        });
        const data = await response.json();
        state.points = data.points;
        addHistory(`Mirrored ${axis}`);
        redraw();
    } catch (error) {
        console.error('Mirror error:', error);
    }
}

// ============= UI INTERACTIONS =============
function showRotateDialog() {
    showModal('Rotation', 'Enter angle (degrees):', (value) => {
        rotateShape(parseFloat(value));
    });
}

function showScaleDialog() {
    showModal('Scale', 'Enter scale factor (e.g. 1.5):', (value) => {
        scaleShape(parseFloat(value));
    });
}

function showMoveDialog() {
    showModal('Move', 'Enter X offset:', (xValue) => {
        showModal('Move', 'Enter Y offset:', (yValue) => {
            movePoints(parseFloat(xValue), parseFloat(yValue));
        });
    });
}

function movePoints(dx, dy) {
    state.points = state.points.map(p => [p[0] + dx, p[1] + dy]);
    addHistory(`Moved (${dx}, ${dy})`);
    redraw();
}

function finishShape() {
    if (state.points.length >= 3) {
        analyzeShape();
        state.shapes.push({
            points: [...state.points],
            color: state.currentColor,
            finished: true
        });
        state.selectedShape = state.shapes.length - 1;
        addHistory(`Finished ${state.currentShape}`);
        state.points = [];
        updateUI();
        redraw();
        updateStatus('✓ Shape finished!');
    } else {
        alert('Need at least 3 points to finish!');
    }
}

function saveDrawing() {
    if (state.points.length === 0 && state.shapes.length === 0) {
        alert('Nothing to save!');
        return;
    }

    const timestamp = new Date().toLocaleString();
    const filename = `drawing_${Date.now()}.json`;

    const data = {
        timestamp: timestamp,
        shapes: state.shapes,
        currentShape: state.currentShape,
        currentColor: state.currentColor
    };

    // Download as JSON
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(data, null, 2)));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);

    addHistory(`Saved: ${filename}`);
    updateStatus('✓ Saved!');
}

function clearAll() {
    state.points = [];
    state.shapes = [];
    state.history = [];
    state.selectedShape = null;
    updateHistoryList();
    updateUI();
    redraw();
    updateStatus('Cleared');
}

function undo() {
    if (state.points.length > 0) {
        state.points.pop();
    } else if (state.shapes.length > 0) {
        state.shapes.pop();
    }
    updateUI();
    redraw();
    addHistory('Undo');
}

// ============= HISTORY & STATUS =============
function addHistory(action) {
    const timestamp = new Date().toLocaleTimeString();
    state.history.push(`${timestamp} - ${action}`);
    updateHistoryList();
}

function updateHistoryList() {
    const list = document.getElementById('history-list');
    if (state.history.length === 0) {
        list.innerHTML = '<p class="empty-state">No actions yet</p>';
        return;
    }
    list.innerHTML = state.history
        .slice(-10)
        .map((h, i) => `<div class="history-item">${h}</div>`)
        .join('');
}

function updateStatus(message) {
    document.getElementById('status').textContent = message;
}

// ============= UI UPDATES =============
function resetUI() {
    document.querySelectorAll('.shape-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-shape="${state.currentShape}"]`).classList.add('active');
}

function setDefaultActiveShape() {
    document.querySelector(`[data-shape="${state.currentShape}"]`).classList.add('active');
    document.querySelector(`[data-color="${state.currentColor}"]`).classList.add('active');
}

function updateUI() {
    document.getElementById('stat-points').textContent = state.points.length;
    document.getElementById('stat-mode').textContent = state.currentShape;
    updateHistoryList();
}

function updateColorDisplay() {
    document.getElementById('stat-color').style.color = state.currentColor;
}

// ============= MODAL =============
let modalCallback = null;

function showModal(title, message, callback) {
    modalCallback = callback;
    document.getElementById('modal-title').textContent = title;
    const input = document.getElementById('modal-input');
    input.placeholder = message;
    input.value = '';
    document.getElementById('modal').style.display = 'flex';
    input.focus();
}

function hideModal() {
    document.getElementById('modal').style.display = 'none';
    modalCallback = null;
}

function handleModalOk() {
    const value = document.getElementById('modal-input').value;
    if (value && modalCallback) {
        modalCallback(value);
    }
    hideModal();
}

// ============= UTILS =============
function snapToGrid(value) {
    return Math.round(value / GRID_SIZE) * GRID_SIZE;
}
