from flask import render_template, request, jsonify, Blueprint
from utils import make_dict
import openai
from dotenv import dotenv_values


bp = Blueprint("chatbot", __name__)
 
@bp.route('/chatbot')
def chat_bot():
    return render_template("chatbot/chatbot.html",data=make_dict("chatbot"))

@bp.route("/chat", methods=["POST"])
def chat():
    global ENV_PATH
    env_path = ENV_PATH
    config = dotenv_values(env_path)
    # OPENAI_API_KEY を取得
    openai.api_key = config.get("OPENAI_API_KEY")
    data = request.get_json()
    user_message = data.get("message", "")
    try:
        # OpenAI API で応答を取得
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # または `gpt-4`
            messages=[{"role": "user", "content": user_message}]
        )

        ai_response = response["choices"][0]["message"]["content"]
    except Exception as e:
        ai_response = "エラーが発生しました。管理者へお伝えください。"

    return jsonify({"response": ai_response})
