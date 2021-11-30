from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from app.models.dfvalue import DataFrameValue

# Flaskの定義
app = Flask(__name__, template_folder='../views')


# サーバ停止時にセッションを切断
@app.teardown_appcontext
def remove_session(ex=None):
    from app.models.base import Session
    Session.remove()


# 「ホーム」へのルーティング
@app.route('/')
def index():
    return render_template('./index.html')


# 「当サイトについて」へのルーティング
@app.route('/about')
def about():
    return render_template('./about.html')


# フロントエンドにレスポンスを返すAPIを定義
@app.route('/api/value/', methods=['GET'])
def api_make_handler():
    duration = request.args.get('duration')
    if not duration:
        duration = '1Y'
    df = DataFrameValue(duration)
    df.set_all_values()
    return jsonify(df.dict), 200


# サーバを起動
def start():
    app.run(threaded=True)
