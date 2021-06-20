import os
from flask.json import jsonify
from flask.views import MethodView
# from flask import render_template
from flask import request
from flask import send_file
from PIL import Image
from PIL import ImageDraw
from src.service.image_process import ImageProcess
# from flask import current_app


class ImageAnalysisController(MethodView):
    """ 画像分析コントローラー
    """
    def analysisAction():
        """visionAPIで分析
        """
        # ファイルがアップロードされているか
        inputTypeFileName: str = 'image-input'
        if inputTypeFileName not in request.files:
            return jsonify({'result': 'uploadFile is required.'})

        imgFile = request.files[inputTypeFileName]
        imgName = imgFile.filename

        # ファイル名がなければNG
        if '' == imgName:
            return jsonify({'result': 'filename must not empty.'})

        # ファイル保存
        imgFile.save(os.path.join("secret/", imgName))

        # 画像からラベル取得
        imageProcess = ImageProcess
        labelList: list[str] = imageProcess.getLabels("secret/" + imgName)
        # 画像からテキスト認識
        # labelList: list[any] = []
        # imageProcess.detectText("secret/" + imgName)
        # labelList = imageProcess.detectDocumentText("secret/" + imgName)

        # JSONを返す
        return jsonify({'response': labelList})
        # テンプレートをレンダリング
        # return render_template('imageAnalysis.html', title='Image Analysis Result')
        # 画像をダウンロードさせる
        # return send_file('secret/' + imgName, attachment_filename=imgName, as_attachment=True, mimetype='image/jpeg')

    def drawDetectTextaction():
        """ 認識した範囲を描画して画像を返す
        """
        imgFile = request.files['image-input']
        imgName = imgFile.filename
        imgFile.save(os.path.join("secret/", imgName))
        imageProcess: ImageProcess = ImageProcess
        drawList: list[any] = imageProcess.detectDocumentText("secret/" + imgName)

        # 画像に描画する
        img = Image.open("secret/" + imgName)
        d = ImageDraw.Draw(img)
        for one in drawList:
            d.rectangle(one, outline='green', width=3)
        img.save('secret/convert.jpg', quality=95)
        return send_file('secret/convert.jpg', attachment_filename=imgName, as_attachment=True, mimetype='image/jpeg')
