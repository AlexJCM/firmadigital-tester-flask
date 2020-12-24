import os
from base64 import b64decode
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/rest', methods=['POST'])
def grabar_archivos_firmados():
    # def grabar_archivos_firmados(set_var_usuario, set_var_documento, set_var_archivo, set_var_datos_firmante, set_var_fecha,
    #       set_var_institucion, set_var_cargo):
    if not request.json:
        abort(400)

    set_var_documento = request.json['nombreDocumento']
    set_var_archivo = request.json['archivo']    

    fecha_actual = datetime.now().strftime('%Y%m%d%H%I%S')
    carpeta = '/home/alexjcm/Documentos/Pasantias_Desarrollo/firmaEC/firmadigital-tester-flask/rest/tmp' + fecha_actual
    print('documento: ', set_var_documento)
    print('carpeta: ', carpeta)
    # print('archivo: ', set_var_archivo)
    
    if not os.path.isdir(carpeta):
        os.mkdir(carpeta)

    ruta_destino_archivo = os.path.join(carpeta, set_var_documento)
    file_decode = b64decode(set_var_archivo, validate=True)
    # print('file_decode: ', file_decode)
    # Grabamos en el servidor
    archivo_ok = open(ruta_destino_archivo, 'wb')
    archivo_ok.write(file_decode)
    archivo_ok.close()

    # Retorno de bandera para el servicio web
    if archivo_ok:
        return 'OK'  # Se recibió el documento
    else:
        return 'ERROR'  # No se recibió el documento


if __name__ == '__main__':
    app.run(debug=True)
