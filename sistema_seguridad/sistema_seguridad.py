# sistema_seguridad.py
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
SECRET_KEY = "RJkvfT6wGkPVEki8zwPBT8scLfl4qNOs"

@app.route('/validar-token', methods=['POST'])
def validar_token():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token no proporcionado'}), 401
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'valido': True, 'usuario': payload}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Token invalido'}), 401

if __name__ == '__main__':
    app.run(port=5003)
