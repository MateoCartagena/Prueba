from flask import Flask, Response, request
from spyne import Application, ServiceBase, Integer, Unicode, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import xml.etree.ElementTree as ET
import html

app = Flask(__name__)

class CertificacionService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def registrar_certificacion(ctx, idSolicitud):
        # Aquí podrías incluir lógica real para verificar en una base de datos, etc.
        if idSolicitud > 0:
            return "<cert:status>success</cert:status>"
        else:
            return "<cert:status>error</cert:status>"

soap_app = Application(
    [CertificacionService],
    tns='example.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(soap_app)

@app.route('/certificacion', methods=['GET', 'POST'])
def soap():
    def start_response(status, headers):
        return Response(response=None, status=status, headers=headers)

    response = wsgi_app(request.environ, start_response)
    return Response(response, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
