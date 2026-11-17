from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # <--- ЭТА СТРОКА ОБЯЗАТЕЛЬНА
import requests

app = Flask(__name__)
CORS(app)  # <--- И ЭТА СТРОКА ОБЯЗАТЕЛЬНА
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Пока оставляем пустым, ключ вставим чуть позже
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_KEY", "твой_ключ_будет_здесь")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct", 
                "messages": [{"role": "user", "content": user_message}]
            }
        )
        # Берем ответ от ИИ
        ai_reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": "Ошибка сервера: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
