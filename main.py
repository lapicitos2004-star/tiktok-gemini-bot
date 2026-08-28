import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Leemos la API Key desde las variables ocultas del servidor por seguridad
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/webhook', methods=['POST'])
def handle_tikops_command():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400
        
    usuario = data.get("usuario", "Espectador")
    pregunta = data.get("pregunta", "")
    
    if not pregunta:
        return jsonify({"message": f"@{usuario}, ¡dime qué quieres preguntarle a Ares!"})
        
    try:
        # Instrucciones estrictas para que la IA responda muy corto
        prompt = f"Responde de forma muy corta (máximo 140 caracteres), natural y en español a esta pregunta de un espectador de mi directo llamado {usuario}: {pregunta}"
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        respuesta_chat = f"🤖 @{usuario}: {response.text}"
        return jsonify({"message": respuesta_chat}), 200
        
    except Exception as e:
        return jsonify({"message": f"@{usuario}, Ares está descansando ahora mismo..."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
