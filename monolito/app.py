from flask import Flask, render_template_string
import mysql.connector
import time

app = Flask(__name__)

# Configuración de acceso a datos (Monolítica)
db_config = {
    'host': 'db-tarea-ia.c3oshhympms4.us-east-1.rds.amazonaws.com',
    'port': 3306,
    'user': 'admin',
    'password': '12345678', 
    'database': 'mysql',
    'ssl_ca': 'global-bundle.pem'
}

@app.route('/')
def index():
    start_time = time.time()
    try:
        # ACCESO A DATOS
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        # LÓGICA: Simulación de carga para el Stress Test
        # Esto consumirá CPU para que el test sea visible
        res = 0
        for i in range(100000):
            res += i
            
        cursor.close()
        conn.close()
        
        # INTERFAZ (HTML Embebido)
        return render_template_string('''
            <div style="font-family: Arial; text-align: center; margin-top: 50px;">
                <h1 style="color: #2c3e50;">Aplicación Monolítica - IA & Troubleshooting</h1>
                <p><strong>Estado:</strong> Conectado a RDS exitosamente ✅</p>
                <p><strong>Versión BD:</strong> {{ version }}</p>
                <p><strong>Tiempo de respuesta:</strong> {{ timing }} ms</p>
                <hr style="width: 50%;">
                <small>Calculando lógica pesada... Resultado: {{ total }}</small>
            </div>
        ''', version=db_version[0], timing=round((time.time()-start_time)*1000, 2), total=res)

    except Exception as e:
        return f"<h1>Error de conexión</h1><p>{str(e)}</p>", 500

if __name__ == '__main__':
    # Ejecutamos en el puerto 8080 que ya abriste en el Security Group
    app.run(host='0.0.0.0', port=8080)
