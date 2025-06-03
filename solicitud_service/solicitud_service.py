# solicitud_service.py
from flask import Flask, request, jsonify
import requests
import xml.etree.ElementTree as ET
import html

app = Flask(__name__)

VALIDAR_TOKEN_URL = "http://localhost:5003/validar-token"
SOAP_URL = "http://localhost:5002/certificacion"

solicitudes = {}
ultimo_id = 0

def validar_token_externamente(token):
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.post(VALIDAR_TOKEN_URL, headers=headers, timeout=5)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("valido"):
                return json_response.get("usuario")
            else:
                return None
        else:
            return None
    except requests.RequestException:
        return None


def llamar_servicio_soap(solicitud_id):
    soap_request = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cert="http://certificacion.example.com/">
       <soapenv:Body>
          <cert:registrar_certificacion>
             <cert:idSolicitud>{solicitud_id}</cert:idSolicitud>
          </cert:registrar_certificacion>
       </soapenv:Body>
    </soapenv:Envelope>
    """
    headers = {'Content-Type': 'text/xml'}
    try:
        response = requests.post(SOAP_URL, data=soap_request, headers=headers, timeout=5)
        if response.status_code != 200:
            return "rechazado"
        
        # Parsear la respuesta XML
        root = ET.fromstring(response.content)
        # Usar namespaces para buscar el elemento correcto (ajusta según tu XML)
        ns = {
            'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
            'tns': 'example.soap'
        }
        # Encontrar el elemento registrar_certificacionResult
        result_elem = root.find('.//tns:registrar_certificacionResult', ns)
        if result_elem is None:
            return "rechazado"

        # El texto está escapado, des-escaparlo
        contenido = html.unescape(result_elem.text)

        # Ahora buscar el texto success
        if "<cert:status>success</cert:status>" in contenido:
            return "procesado"
        else:
            return "rechazado"
    except Exception as e:
        print("Error llamando al servicio SOAP:", e)
        return "rechazado"

@app.route('/solicitudes', methods=['POST'])
def crear_solicitud():
    auth_header = request.headers.get('Authorization', '')
    # print("Auth Header:", auth_header)

    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token no proporcionado'}), 401
    
    token = auth_header.split(' ')[1]
    usuario = validar_token_externamente(token)
    # print("Usuario:", usuario)

    
    if not usuario:
        return jsonify({'error': 'Token inválido'}), 401
    
    # Asumamos que el payload tiene el nombre en usuario['name'] o similar
    nombre_estudiante = usuario.get('name')
    if not nombre_estudiante:
        return jsonify({'error': 'Nombre de usuario no encontrado en token'}), 400
    
    data = request.get_json()
    # print("Payload recibido:", data)

    if not data or 'tipo_solicitud' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400

    global ultimo_id
    ultimo_id += 1

    solicitud = {
        'id': ultimo_id,
        'estudiante': nombre_estudiante,  # ✅ usar la variable correcta
        'tipo_solicitud': data['tipo_solicitud'],
        'estado': 'en revisión',
    }


    solicitudes[ultimo_id] = solicitud

    estado_final = llamar_servicio_soap(ultimo_id)
    solicitud['estado'] = estado_final

    return jsonify(solicitud), 201


@app.route('/solicitudes/<int:solicitud_id>', methods=['GET'])
def obtener_solicitud(solicitud_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token no proporcionado'}), 401
    
    token = auth_header.split(' ')[1]
    usuario = validar_token_externamente(token)
    if not usuario:
        return jsonify({'error': 'Token invalido'}), 401

    solicitud = solicitudes.get(solicitud_id)
    if not solicitud:
        return jsonify({'error': 'Solicitud no encontrada'}), 404
    
    return jsonify(solicitud), 200

if __name__ == '__main__':
    app.run(port=5004)
