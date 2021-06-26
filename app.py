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


if __name__ == '__main__':
    # app.run(host="127.0.0.1", port=5000, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
