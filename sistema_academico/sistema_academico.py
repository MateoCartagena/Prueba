# sistema_academico.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos simulada
solicitudes = {}

@app.route('/solicitudes', methods=['POST'])
def crear_solicitud():
    data = request.json
    solicitud_id = len(solicitudes) + 1
    data['id'] = solicitud_id
    data['estado'] = 'en revisión'
    solicitudes[solicitud_id] = data
    return jsonify(data), 201

@app.route('/solicitudes/<int:solicitud_id>', methods=['GET'])
def obtener_solicitud(solicitud_id):
    solicitud = solicitudes.get(solicitud_id)
    if solicitud:
        return jsonify(solicitud), 200
    return jsonify({'error': 'Solicitud no encontrada'}), 404

if __name__ == '__main__':
    app.run(port=5001)
