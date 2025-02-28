from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL del webhook de n8n
N8N_WEBHOOK_URL = "https://tudominio.n8n.cloud/webhook/12345"

@app.route('/consultar', methods=['POST'])
def consultar_producto():
    data = request.json
    consulta = data.get('consulta')

    if not consulta:
        return jsonify({"error": "Por favor, proporciona una consulta."}), 400

    # Hacer la petición a n8n y aumentar timeout a 30s (por si tarda en responder)
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"consulta": consulta},
            timeout=30  # Aumentar tiempo de espera
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return jsonify({"error": "Tiempo de espera agotado. Intenta de nuevo más tarde."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al conectar con n8n: {str(e)}"}), 500

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
