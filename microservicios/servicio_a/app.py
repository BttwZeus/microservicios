from flask import Flask, request, render_template_string, jsonify
import mysql.connector
import requests
import os

app = Flask(__name__)

# Configuración por variables de entorno (Requisito: no hardcoded) [cite: 56]
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_ca='global-bundle.pem'
    )

@app.route('/')
def index():
    # Interfaz HTML [cite: 42]
    return render_template_string('''
        <h1>Registro de Usuario - Servicio A</h1>
        <form action="/registrar" method="post">
            Nombre: <input type="text" name="nombre" required><br>
            Email: <input type="email" name="email" required><br>
            <button type="submit">Registrar</button>
        </form>
    ''')

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    
    try:
        # 1. Guardar en Tabla A [cite: 43]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios_aguirre (nombre, email) VALUES (%s, %s)", (nombre, email))
        conn.commit()
        cursor.close()
        conn.close()

        # 2. Llamar al Servicio B (HTTP Interno) [cite: 44, 80]
        # Usamos el nombre del servicio 'servicio_b' como host gracias a Docker Compose [cite: 81]
        try:
            response_b = requests.post('http://servicio_b:5001/procesar', json={'usuario': nombre}, timeout=3)
            msg_b = response_b.json().get('mensaje')
        except:
            # Manejo de resiliencia si B está caído [cite: 45, 90]
            msg_b = "Servicio B en mantenimiento. El registro se procesará después."

        return jsonify({
            "status": "success",
            "mensaje": "Usuario guardado en Servicio A",
            "notificacion_b": msg_b
        })

    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
