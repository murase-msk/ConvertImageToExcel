import os
from typing import Dict, List
from flask.json import jsonify
from flask.views import MethodView
from flask import render_template
from flask import request
from flask import send_file
from PIL import Image
from PIL import ImageDraw
from src.service.excel_process import ExcelData, ExcelProcess
from src.service.image_process import Block, ImageProcess, Word
# from flask import current_app
import pdf2image


class ImageAnalysisController(MethodView):
    """ 画像分析コントローラー
    """

    def analysisDocumentAction():
        """ テキスト分析
        """
        imgFile = request.files['image-input']
        imgName = imgFile.filename
        imgFile.save(os.path.join("secret/tmpImage/", imgName))
        imageProcess: ImageProcess = ImageProcess()
        # 画像データをGoogleVisionAPIのdetectDocumentで解析
        analysisDocumentList: Dict[List[Block], List[Word]] = imageProcess.detectDocumentTextV2("secret/tmpImage/" + imgName)
        # {"blocks":[{"text":???, "p0":{"x":?,"y":?}, "p1":???, "p2":???, "p3":???, "confidence":???}, ... ], "words":[{...}]}
        excelProcess: ExcelProcess = ExcelProcess()
        # Excelに入るように位置調整する
        # 一番小さい文字の高さを1セルの高さに設定
        # 1セルの高さが決まったらそれに応じてセルに割り当てる
        # 文字の中心がどのセルに入るか割り当てる
        outputExcelData: List[ExcelData] = excelProcess.mappingFromPixelCoordinatesToExcelCoordinates(analysisDocumentList["words"])
        excelProcess.writeExcel(outputExcelData)
        # Excelへ出力
        return excelProcess.getResponse()

    def analysisPdfDocumentAction():
        """ テキスト分析(PDF)
        """
        imgFile = request.files['pdf-input']
        imgName = imgFile.filename
        imgFile.save(os.path.join("secret/tmpImage/", imgName))
        imageProcess: ImageProcess = ImageProcess()
        # 画像データをGoogleVisionAPIのdetectDocumentで解析
        analysisDocumentList: Dict[List[Block], List[Word]] = imageProcess.detectDocumentTextForPdf("secret/tmpImage/" + imgName)
        excelProcess: ExcelProcess = ExcelProcess()
        # Excelに入るように位置調整する
        outputExcelData: List[ExcelData] = excelProcess.mappingFromPixelCoordinatesToExcelCoordinates(analysisDocumentList["words"])
        excelProcess.writeExcel(outputExcelData)
        # Excelへ出力
        return excelProcess.getResponse()

    def getLabelAction():
        """visionAPIでラベルを取得
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
        imgFile.save(os.path.join("secret/tmpImage/", imgName))

        # 画像からラベル取得
        imageProcess = ImageProcess()
        labelList: list[str] = imageProcess.getLabels("secret/tmpImage/" + imgName)

        # JSONを返す
        return jsonify({'response': labelList})
        # テンプレートをレンダリング
        # return render_template('imageAnalysis.html', title='Image Analysis Result')

    def detectTextAction():
        """ テキストを検出する
        """
        imgFile = request.files['image-input']
        imgName = imgFile.filename
        imgFile.save(os.path.join("secret/tmpImage/", imgName))
        imageProcess: ImageProcess = ImageProcess()
        # 画像からテキスト認識
        textList: list[any] = []
        textList = imageProcess.detectText("secret/tmpImage/" + imgName)
        return jsonify({'response': textList})

    def drawDetectTextAction():
        """ 認識した範囲を描画して画像を返す
        """
        imgFile = request.files['image-input']
        imgName = imgFile.filename
        imgFile.save(os.path.join("secret/tmpImage/", imgName))
        imageProcess: ImageProcess = ImageProcess()
        drawList: list[any] = imageProcess.detectDocumentText("secret/tmpImage/" + imgName)

        # 画像に描画する
        img = Image.open("secret/tmpImage/" + imgName)
        d = ImageDraw.Draw(img)
        for one in drawList:
            d.rectangle(one, outline='green', width=3)
        img.save('secret/tmpImage/convert.jpg', quality=95)
        return send_file('secret/tmpImage/convert.jpg', attachment_filename=imgName, as_attachment=True, mimetype='image/jpeg')

    def convertPdfToImgAction():
        """ PDFをJPEG変換し表示する
        """
        imgFile = request.files['pdf-input']
        # imgName = imgFile.filename
        # imgFile.save(os.path.join("secret/tmpImage/", imgName))
        images = pdf2image.convert_from_bytes(imgFile.read())
        convertedFilePath: str = "assets/img/tmp/test.png"
        images[0].save(convertedFilePath)

        return render_template('getImagePositionResultPage.html', title='Image Analysis Result', imagePath="/" + convertedFilePath)

    def textDetectApiV1Action():
        """ BASE64エンコードされたPDFファイルと検出したい文字範囲を受け取って文字認識して返す
        """
        return
