# sistema_certificacion.py
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/certificacion', methods=['POST'])
def certificacion():
    xml_request = request.data.decode('utf-8')

    # Extraer idSolicitud (simple)
    import re
    match = re.search(r'<cert:idSolicitud>(\d+)</cert:idSolicitud>', xml_request)
    id_solicitud = int(match.group(1)) if match else 0

    # Responder éxito para id par, fallo para id impar (simulación)
    if id_solicitud % 2 == 0:
        response_xml = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cert="http://certificacion.example.com/">
            <soapenv:Body>
                <cert:CertificacionResponse>
                    <cert:status>success</cert:status>
                </cert:CertificacionResponse>
            </soapenv:Body>
        </soapenv:Envelope>
        """
    else:
        response_xml = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cert="http://certificacion.example.com/">
            <soapenv:Body>
                <cert:CertificacionResponse>
                    <cert:status>failure</cert:status>
                </cert:CertificacionResponse>
            </soapenv:Body>
        </soapenv:Envelope>
        """

    return Response(response_xml, mimetype='text/xml')

if __name__ == '__main__':
    app.run(port=5002)
