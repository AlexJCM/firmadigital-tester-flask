import os
from base64 import b64decode
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/static/*": {"origins": "*"}})
#CORS(app)


@app.route('/')
def index():
    return "Hola mundo desde servico web rest con Flask!"


@app.route('/rest', methods=['POST'])
def grabar_archivos_firmados():
    # def grabar_archivos_firmados(set_var_usuario, set_var_documento, set_var_archivo, set_var_datos_firmante, set_var_fecha,
    #       set_var_institucion, set_var_cargo):
    if not request.json:
        abort(400)

    set_var_documento = request.json['nombreDocumento']
    set_var_archivo = request.json['archivo']    
      
    carpeta = 'static' # En esta carpeta se almacenarán todos los pdfs  firmados      
    print('documento: ', set_var_documento)
    print('carpeta: ', carpeta)
      
    if not os.path.isdir(carpeta):
        os.mkdir(carpeta)

    ruta_destino_archivo = os.path.join(carpeta, set_var_documento)
    file_decode = b64decode(set_var_archivo, validate=True)
  
    # Grabamos en el servidor
    archivo_ok = open(ruta_destino_archivo, 'wb')
    archivo_ok.write(file_decode)
    archivo_ok.close()

    # Retorno de bandera para el servicio web
    # Retornar el valor en formato Json
    if archivo_ok:
        return jsonify({'result': 'OK'})  # Se recibió el documento
    else:
        return jsonify({'result': 'ERROR'})  # No se recibió el documento


if __name__ == '__main__':
    set_var_documento = ''
    app.run(debug=True, port=3000)
