import os
from flask import Flask
from src.controller.index_controller import IndexController
from src.controller.user_controller import UserController
from src.controller.image_analysis_controller import ImageAnalysisController
from database import init_db
from src.model.model import User
from src.model.settingModel import Setting
import logging
from logging import StreamHandler

app = Flask(__name__)

# 参照するフォルダの指定
app = Flask(__name__, static_folder="assets", template_folder="assets/html")

# ロギング設定
if os.environ['FLASK_ENV'] == 'development':  # 開発環境
    logging.basicConfig(level=logging.INFO)
    # SQLAlchemyのログ出力
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
else:  # 本番環境
    # handler = StreamHandler()
    LOGFILE_NAME = "build/app/DEBUG.log"
    app.logger.setLevel(logging.ERROR)
    app.logger.addHandler(LOGFILE_NAME)

# DB設定
app.config.from_object('config.Config')
init_db(app)

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

app.add_url_rule('/textDetectApiPage', view_func=IndexController.textDetectApiPageAction, methods=['GET'])
app.add_url_rule('/textDetectApi', view_func=ImageAnalysisController.textDetectApiAction, methods=['POST'])

app.add_url_rule('/user/<user_id>', view_func=UserController.userAction, methods=['GET'])
app.add_url_rule('/user/config', view_func=UserController.configAction, methods=['GET'])


# @app.route('/')
# def hello():
#     allUser = User.query.all()
#     user: User = allUser[0]
#     # name = "Hello World"
#     return user.name


if __name__ == '__main__':
    #
    if os.environ['FLASK_ENV'] == 'development':
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        #app.run(host="127.0.0.1", port=3031, debug=False)
        app.run()
