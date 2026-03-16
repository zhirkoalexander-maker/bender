from flask import Flask, render_template, jsonify, request
import math
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# Store drawings in memory (in production, use database)
drawings = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_shape():
    """Analyze geometric shape"""
    data = request.json
    points = data.get('points', [])
    
    if len(points) < 2:
        return jsonify({'error': 'Need at least 2 points'}), 400
    
    # Calculate sides
    sides = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        sides.append(dist)
    
    # Calculate perimeter
    perimeter = sum(sides)
    
    # Calculate area using Shoelace formula
    area = 0
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        area += p1[0] * p2[1] - p2[0] * p1[1]
    area = abs(area) / 2
    
    # Determine shape type
    n = len(points)
    shape_type = "Polygon"
    
    if n == 3:
        shape_type = "Triangle"
    elif n == 4:
        # Check if square or rectangle
        sides_sorted = sorted(sides)
        if all(abs(s - sides_sorted[0]) < 10 for s in sides_sorted):
            shape_type = "Square"
        elif abs(sides_sorted[0] - sides_sorted[1]) < 10 and abs(sides_sorted[2] - sides_sorted[3]) < 10:
            shape_type = "Rectangle"
        else:
            shape_type = "Quadrilateral"
    
    return jsonify({
        'shape_type': shape_type,
        'vertices': n,
        'sides': sides,
        'perimeter': round(perimeter, 2),
        'area': round(area, 2),
        'analysis': f"{shape_type}\nVertices: {n}\nPerimeter: {perimeter:.1f}\nArea: {area:.1f}"
    })

@app.route('/api/save', methods=['POST'])
def save_drawing():
    """Save drawing"""
    data = request.json
    timestamp = datetime.now().isoformat()
    drawing = {
        'id': len(drawings),
        'timestamp': timestamp,
        'data': data
    }
    drawings.append(drawing)
    return jsonify({'success': True, 'id': drawing['id']})

@app.route('/api/drawings', methods=['GET'])
def get_drawings():
    """Get all saved drawings"""
    return jsonify(drawings)

@app.route('/api/rotate', methods=['POST'])
def rotate_points():
    """Rotate shape"""
    data = request.json
    points = data['points']
    angle = data['angle']
    
    # Find center
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    
    # Rotate
    rad = math.radians(angle)
    rotated = []
    for x, y in points:
        nx = cx + (x - cx) * math.cos(rad) - (y - cy) * math.sin(rad)
        ny = cy + (x - cx) * math.sin(rad) + (y - cy) * math.cos(rad)
        rotated.append([nx, ny])
    
    return jsonify({'points': rotated})

@app.route('/api/scale', methods=['POST'])
def scale_points():
    """Scale shape"""
    data = request.json
    points = data['points']
    factor = data['factor']
    
    # Find center
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    
    # Scale
    scaled = []
    for x, y in points:
        nx = cx + (x - cx) * factor
        ny = cy + (y - cy) * factor
        scaled.append([nx, ny])
    
    return jsonify({'points': scaled})

@app.route('/api/mirror', methods=['POST'])
def mirror_points():
    """Mirror shape"""
    data = request.json
    points = data['points']
    axis = data['axis']  # 'horizontal' or 'vertical'
    
    mirrored = []
    if axis == 'horizontal':
        cy = sum(p[1] for p in points) / len(points)
        mirrored = [[x, 2*cy - y] for x, y in points]
    else:  # vertical
        cx = sum(p[0] for p in points) / len(points)
        mirrored = [[2*cx - x, y] for x, y in points]
    
    return jsonify({'points': mirrored})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
