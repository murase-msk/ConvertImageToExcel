import os
from flask import Flask
from src.controller.index_controller import IndexController
from src.controller.user_controller import UserController
from src.controller.image_analysis_controller import ImageAnalysisController

app = Flask(__name__)

# 参照するフォルダの指定
app = Flask(__name__, static_folder="assets", template_folder="assets/html")

# 環境変数設定(上書きする)
app.config.from_pyfile('./secret/.env_dev')
# google Vision API キー設定
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = app.config['GOOGLE_APPLICATION_CREDENTIALS']

# ファイルアップロード制限 : 3MB
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024


app.add_url_rule('/', view_func=IndexController.indexAction, methods=['GET'])
app.add_url_rule('/file-upload', view_func=ImageAnalysisController.analysisAction, methods=['POST'])

app.add_url_rule('/drawDetectedText', view_func=IndexController.drawDetectedTextPageAction, methods=['GET'])
app.add_url_rule('/drawDetectedText/file-upload', view_func=ImageAnalysisController.drawDetectTextaction, methods=['POST'])
app.add_url_rule('/user/<user_id>', view_func=UserController.userAction, methods=['GET'])
app.add_url_rule('/user/config', view_func=UserController.configAction, methods=['GET'])


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
