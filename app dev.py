# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # For cross-origin requests

# deepseek_api.py
# from deepseek import ChatDeepSeek

# llm = ChatDeepSeek(
#     model="deepseek-chat",
#     api_key="your-api-key-here",
#     temperature=0.7,
#     timeout=15
# )


from openai import OpenAI

client = OpenAI(api_key="sk-dba351629c004c41b3c4c99c9e806db4", base_url="https://api.deepseek.com")


def get_ai_response(user_input):
    #response = llm.invoke([("human", user_input)])
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": user_input},
        ],
        stream=False
    )

    #return response.content
    return response.choices[0].message.content

app = Flask(__name__)
CORS(app)  # Enable CORS for development

@app.route('/chat', methods=['POST'])
def chat_handler():
    user_message = request.json.get('msg')
    try:
        # Process message with your AI
        response = get_ai_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)