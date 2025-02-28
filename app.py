from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL del webhook de n8n
N8N_WEBHOOK_URL = "https://n8n-n8n-danielvtoth.qwquli.easypanel.host/webhook/81de7001-3a8a-4f4c-8a31-8d327f41ee09"  # Reemplaza con tu URL de webhook

@app.route('/')
def home():
    return "¡Bienvenido a la aplicación Flask conectada a n8n!"

@app.route('/consultar', methods=['POST'])
def consultar_producto():
    # Obtener la consulta del usuario desde el cuerpo de la solicitud
    data = request.json
    consulta = data.get('consulta')

    if not consulta:
        return jsonify({"error": "Por favor, proporciona una consulta."}), 400

    # Enviar la consulta a n8n mediante un webhook
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"consulta": consulta}
        )
        response.raise_for_status()  # Lanza una excepción si la solicitud falla
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al conectar con n8n: {str(e)}"}), 500

    # Devolver la respuesta de n8n al usuario
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
