from flask import Flask, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_ca='global-bundle.pem'
    )

@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.get_json()
    usuario = data.get('usuario')

    # Lógica costosa real (Simulación) [cite: 48]
    # Guardar en una tabla diferente a la de A [cite: 49]
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Simulamos procesamiento
        time.sleep(2) 
        cursor.execute("INSERT INTO logs_procesamiento (usuario, detalle) VALUES (%s, %s)", (usuario, "Procesado por Servicio B"))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"status": "ok", "mensaje": "Notificación enviada al Servicio B"}) # [cite: 58]
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500

if __name__ == '__main__':
    # Puerto diferente para comunicación interna [cite: 54]
    app.run(host='0.0.0.0', port=5001)
