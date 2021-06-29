# import os
from flask import Flask
from src.controller.index_controller import IndexController
from src.controller.user_controller import UserController
from src.controller.image_analysis_controller import ImageAnalysisController
from database import init_db
from src.model.model import User

app = Flask(__name__)

# 参照するフォルダの指定
app = Flask(__name__, static_folder="assets", template_folder="assets/html")

# DB設定
app.config.from_object('config.Config')
init_db(app)

# 環境変数設定(上書きする)
# app.config.from_pyfile('./secret/.env_dev')
# google Vision API キー設定
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = app.config['GOOGLE_APPLICATION_CREDENTIALS']
# MySQL環境変数設定
# os.environ['MYSQL_USER'] = app.config['MYSQL_USER']
# os.environ['MYSQL_PASSWORD'] = app.config['MYSQL_PASSWORD']
# os.environ['MYSQL_HOST'] = app.config['MYSQL_HOST']
# os.environ['MYSQL_DATABASE'] = app.config['MYSQL_DATABASE']

# ファイルアップロード制限 : 3MB
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024


app.add_url_rule('/', view_func=IndexController.indexAction, methods=['GET'])
app.add_url_rule('/file-upload', view_func=ImageAnalysisController.analysisDocumentAction, methods=['POST'])
app.add_url_rule('/file-upload-pdf', view_func=ImageAnalysisController.analysisPdfDocumentAction, methods=['POST'])

app.add_url_rule('/drawDetectedText', view_func=IndexController.drawDetectedTextPageAction, methods=['GET'])
app.add_url_rule('/drawDetectedText/file-upload', view_func=ImageAnalysisController.drawDetectTextAction, methods=['POST'])

app.add_url_rule('/getLabel', view_func=IndexController.getLabelPageAction, methods=['GET'])
app.add_url_rule('/getLabel/file-upload', view_func=ImageAnalysisController.getLabelAction, methods=['POST'])

app.add_url_rule('/detectText', view_func=IndexController.detectTextPageAction, methods=['GET'])
app.add_url_rule('/detectText/file-upload', view_func=ImageAnalysisController.detectTextAction, methods=['POST'])

app.add_url_rule('/getImagePosition', view_func=IndexController.getImagePositionPageAction, methods=['GET'])
app.add_url_rule('/getImagePosition/file-upload', view_func=ImageAnalysisController.convertPdfToImgAction, methods=['POST'])

app.add_url_rule('/textDetectApi', view_func=IndexController.textDetectApiPageAction, methods=['GET'])
app.add_url_rule('/textDetectApi/v1', view_func=ImageAnalysisController.textDetectApiV1Action, methods=['POST'])

app.add_url_rule('/user/<user_id>', view_func=UserController.userAction, methods=['GET'])
app.add_url_rule('/user/config', view_func=UserController.configAction, methods=['GET'])


@app.route('/')
def hello():
    allUser = User.query.all()
    user: User = allUser[0]
    # name = "Hello World"
    return user.name


if __name__ == '__main__':
    # app.run(host="127.0.0.1", port=5000, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
