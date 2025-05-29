# sistema_academico.py
from flask import Flask, jsonify, request

app = Flask(__name__)

estudiantes = {
    "1": {
        "id": "1",
        "name": "Juan Perez"
    }
}

next_id = 2

@app.route('/students', methods=['POST'])
def crear_estudiante():
    global next_id
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'El campo "name" es obligatorio'}), 400

    student_id = str(next_id)
    next_id += 1

    estudiante = {
        'id': student_id,
        'name': data['name']
    }
    estudiantes[student_id] = estudiante
    return jsonify(estudiante), 201

@app.route('/students/<student_id>', methods=['GET'])
def obtener_estudiante(student_id):
    estudiante = estudiantes.get(student_id)
    if estudiante:
        return jsonify(estudiante), 200
    return jsonify({'error': 'Estudiante no encontrado'}), 404

if __name__ == '__main__':
    app.run(port=5001)
