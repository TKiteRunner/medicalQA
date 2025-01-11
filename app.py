from flask import Flask, request, jsonify
from flask_cors import CORS
from kbqa_test import KBQA
import requests
import json

# Translator class
class Translator:
    def __init__(self, api_key, base_url, model):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def translate(self, messages, temperature=0.7):
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json().get("choices")[0].get("message", {}).get("content", "").strip()
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise Exception(f"An error occurred: {err}")

# Flask app
app = Flask(__name__)
CORS(app)

qa_system = KBQA()
translator = Translator(
    api_key="c3dc550d-ae81-42a5-bf63-4fc1bddac1c1",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    model="ep-20241231020502-wfrtb"
)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Medical QA System API. Use the /ask endpoint to ask questions."})

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        question = data.get('question', '')
        language = data.get('language', 'zh')
        mode = data.get('mode', 1)  # 默认模式 1

        if language not in ['zh', 'en', 'ms']:
            return jsonify({"answer": "Invalid language parameter. Supported values are 'zh', 'en', 'ms'."}), 400

        if not question:
            return jsonify({"answer": "请输入您的问题！" if language == "zh" else "Please enter a question!"}), 400

        # Step 1: Translate question to Chinese if needed
        if language in ['en', 'ms']:
            messages = [
                {"role": "system", "content": "Translate the following question to Chinese."},
                {"role": "user", "content": question}
            ]
            question = translator.translate(messages)

        # Step 2: Handle different modes
        if mode == 1:
            # Directly query the knowledge graph
            answer = qa_system.qa_main(question)
        elif mode == 2:
            # Query the knowledge graph and refine the answer
            answer = qa_system.qa_main(question)
            if answer:
                messages = [
                    {"role": "system", "content": "Refine the following answer to make it more conversational."},
                    {"role": "user", "content": answer}
                ]
                answer = translator.translate(messages)
        elif mode == 3:
            # Directly use the large language model to generate an answer
            messages = [
                {"role": "system", "content": "You are a helpful assistant. Please answer the following question."},
                {"role": "user", "content": question}
            ]
            answer = translator.translate(messages)
        else:
            return jsonify({"answer": "Invalid mode parameter. Supported values are 1, 2, or 3."}), 400

        # Step 3: Translate the answer back to English or Malay if needed
        if language in ['en', 'ms']:
            target_lang = "English" if language == "en" else "Malay"
            messages = [
                {"role": "system", "content": f"Translate the following answer to {target_lang}."},
                {"role": "user", "content": answer}
            ]
            answer = translator.translate(messages)

        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"answer": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=True)
