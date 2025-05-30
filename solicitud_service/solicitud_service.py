# solicitud_service.py
from flask import Flask, request, jsonify
import jwt
import requests

app = Flask(__name__)

SECRET_KEY = "mi_clave_secreta"
SOAP_URL = "http://localhost:5002/certificacion"

solicitudes = {}
ultimo_id = 0

def validar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['usuario']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def llamar_servicio_soap(solicitud_id):
    soap_request = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cert="http://certificacion.example.com/">
       <soapenv:Body>
          <cert:CertificacionRequest>
             <cert:idSolicitud>{solicitud_id}</cert:idSolicitud>
          </cert:CertificacionRequest>
       </soapenv:Body>
    </soapenv:Envelope>
    """
    headers = {'Content-Type': 'text/xml'}
    try:
        response = requests.post(SOAP_URL, data=soap_request, headers=headers, timeout=5)
        if response.status_code == 200:
            if "<cert:status>success</cert:status>" in response.text:
                return "procesado"
            else:
                return "rechazado"
        else:
            return "rechazado"
    except requests.RequestException:
        return "rechazado"

@app.route('/solicitudes', methods=['POST'])
def crear_solicitud():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token no proporcionado'}), 401
    
    token = auth_header.split(' ')[1]
    usuario = validar_token(token)
    if not usuario:
        return jsonify({'error': 'Token inválido'}), 401

    data = request.get_json()
    if not data or 'estudiante' not in data or 'tipo_solicitud' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400

    global ultimo_id
    ultimo_id += 1

    solicitud = {
        'id': ultimo_id,
        'estudiante': data['estudiante'],
        'tipo_solicitud': data['tipo_solicitud'],
        'estado': 'en revisión',
        'usuario_solicitante': usuario
    }

    solicitudes[ultimo_id] = solicitud

    # Llamar SOAP para registrar certificación y actualizar estado
    estado_final = llamar_servicio_soap(ultimo_id)
    solicitud['estado'] = estado_final

    return jsonify(solicitud), 201

@app.route('/solicitudes/<int:solicitud_id>', methods=['GET'])
def obtener_solicitud(solicitud_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token no proporcionado'}), 401
    
    token = auth_header.split(' ')[1]
    usuario = validar_token(token)
    if not usuario:
        return jsonify({'error': 'Token inválido'}), 401

    solicitud = solicitudes.get(solicitud_id)
    if not solicitud:
        return jsonify({'error': 'Solicitud no encontrada'}), 404
    
    return jsonify(solicitud), 200

if __name__ == '__main__':
    app.run(port=5004)
