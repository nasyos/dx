from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からOpenAI APIキーを設定
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    sake_type = request.form.get('option1', 'なし')
    sake_taste = request.form.get('option2', 'なし')

    # ChatGPT APIにリクエストを送信
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "あなたは日本酒の専門家です。ユーザーの好みに合わせて日本酒を3本推薦してください。"},
            {"role": "user", "content": f"日本酒の種類: {sake_type}, 味: {sake_taste}のおすすめの日本酒を3本教えてください。それぞれの日本酒について、名前と簡単な説明を提供してください。"}
        ]
    )

    # ChatGPTの回答を取得
    recommendations = response.choices[0].message['content']

    result = f'選択された条件: {sake_type}（{sake_taste}）\n\nおすすめの日本酒:\n{recommendations}'
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)