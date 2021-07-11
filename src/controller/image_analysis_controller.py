from typing import Dict, List
from flask.json import jsonify
from flask.views import MethodView
from flask import render_template
from flask import request
from flask import send_file
from PIL import Image
from PIL import ImageDraw
from shapely.geometry.polygon import Polygon
from src.service.excel_process import ExcelData, ExcelProcess
from src.service.image_process import Block, ImageProcess, SearchArea, Word
from src.service.other_serivce import OtherService
import pdf2image
import base64
import json
import datetime
from src.model.settingModel import Setting


class ImageAnalysisController(MethodView):
    """ 画像分析コントローラー
    """

    def analysisDocumentAction():
        """ テキスト分析
        """
        imgFile = request.files['image-input']
        # imgName = imgFile.filename
        # imgFile.save(os.path.join("secret/tmpImage/", imgName))
        imageProcess: ImageProcess = ImageProcess()
        # 画像データをGoogleVisionAPIのdetectDocumentで解析
        analysisDocumentList: Dict[List[Block], List[Word]] = imageProcess.detectDocumentTextV2ForImage(imgFile.read())
        # analysisDocumentList = {"blocks":[{"text":???, "p0":{"x":?,"y":?}, "p1":???, "p2":???, "p3":???, "confidence":???}, ... ], "words":[{...}]}
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
        # imgName = imgFile.filename
        # imgFile.save(os.path.join("secret/tmpImage/", imgName))
        imageProcess: ImageProcess = ImageProcess()
        # 画像データをGoogleVisionAPIのdetectDocumentで解析
        analysisDocumentList: Dict[List[Block], List[Word]] = imageProcess.detectDocumentTextForPdf(imgFile.read())
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
        # imgFile.save(os.path.join("secret/tmpImage/", imgName))

        # 画像からラベル取得
        imageProcess = ImageProcess()
        labelList: list[str] = imageProcess.getLabels(imgFile.read())

        # JSONを返す
        return jsonify({'response': labelList})
        # テンプレートをレンダリング
        # return render_template('imageAnalysis.html', title='Image Analysis Result')

    def detectTextAction():
        """ テキストを検出する
        """
        imgFile = request.files['image-input']
        # imgName = imgFile.filename
        # imgFile.save(os.path.join("secret/tmpImage/", imgName))
        imageProcess: ImageProcess = ImageProcess()
        # 画像からテキスト認識
        textList: list[any] = []
        textList = imageProcess.detectText(imgFile.read())
        return jsonify({'response': textList})

    def drawDetectTextAction():
        """ 認識した範囲を描画して画像を返す
        """
        # 古い画像を削除
        otherService = OtherService()
        otherService.removeOldFile

        imgFile = request.files['image-input']
        imgName = imgFile.filename
        # imgFile.save(os.path.join("secret/tmpImage/", imgName))
        imageProcess: ImageProcess = ImageProcess()
        drawList: list[any] = imageProcess.detectDocumentText(imgFile.read())

        # 画像に描画する
        # img = Image.open("secret/tmpImage/" + imgName)
        img = Image.open(imgFile)
        d = ImageDraw.Draw(img)
        for one in drawList:
            d.rectangle(one, outline='green', width=3)
        dateStr: str = str(datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S'))
        outputFilePath: str = 'assets/img/tmp/img_' + dateStr + '.jpg'
        img.save(outputFilePath, quality=95)
        return send_file(outputFilePath, attachment_filename=imgName, as_attachment=True, mimetype='image/jpeg')

        # return send_file(img.read(), attachment_filename=imgName, as_attachment=True, mimetype='image/jpeg')

    def convertPdfToImgAction():
        """ PDFをJPEG変換し表示する
        """
        # 古い画像を削除
        otherService = OtherService()
        otherService.removeOldFile()

        imgFile = request.files['pdf-input']
        # imgName = imgFile.filename
        images = pdf2image.convert_from_bytes(imgFile.read())
        dateStr: str = str(datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S'))
        convertedFilePath: str = "assets/img/tmp/img_" + dateStr + ".png"
        images[0].save(convertedFilePath)

        return render_template('getImagePositionResultPage.html', title='Image Analysis Result', imagePath="/" + convertedFilePath)

    def textDetectApiAction():
        """ BASE64エンコードされたPDFファイルと検出したい文字範囲を受け取って文字認識して返す
        """

        # # 本日の使用回数
        # todayUsingNum: int = int(Setting.query.filter_by(setting_name="TodayUsingNum").first().setting_value)
        # # 最終更新日
        # lastUpdate: datetime = Setting.query.filter_by(setting_name="TodayUsingNum").first().updated_at
        # # 1日あたりの上限回数
        # maxDailyUsingNum: int = int(Setting.query.filter_by(setting_name="MaxDailyUsingNum").first().setting_value)

        # if datetime.datetime.strptime(lastUpdate.strftime('%Y/%m/%d'), '%Y/%m/%d') \
        #         < datetime.datetime.strptime(datetime.datetime.now().strftime('%Y/%m/%d'), '%Y/%m/%d'):
        #     # 本日の使用回数をリセットする
        #     todayUsingNumData: Setting = db.session.query(Setting).filter_by(setting_name='TodayUsingNum').first()
        #     todayUsingNum = 0
        #     todayUsingNumData.setting_value = str(todayUsingNum)
        #     db.session.add(todayUsingNumData)
        #     db.session.commit()
        # if todayUsingNum >= maxDailyUsingNum:
        #     return jsonify({'result': ["本日の使用回数が上限に達しました"]})
        # else:
        #     # 本日の使用回数を1増やす
        #     todayUsingNumData: Setting = db.session.query(Setting).filter_by(setting_name='TodayUsingNum').first()
        #     todayUsingNumData.setting_value = str(todayUsingNum + 1)
        #     db.session.add(todayUsingNumData)
        #     db.session.commit()
        # ここまでDB操作

        if not Setting.isAvailableApi():
            return jsonify({'result': ["本日の使用回数が上限に達しました"]})

        jsonData = request.get_json()

        try:
            # テキスト取得範囲を取得する
            searchAreaText = jsonData['searchArea']
            searchAreaList = json.loads(searchAreaText)
            searchAreas: List[SearchArea] = []  # この中に検索エリアのデータが入る
            for searchArea in searchAreaList:
                searchAreas.append(
                    SearchArea(
                        poly=Polygon(
                            [
                                (searchArea["x0"], searchArea["y0"]),
                                (searchArea["x3"], searchArea["y0"]),
                                (searchArea["x3"], searchArea["y3"]),
                                (searchArea["x0"], searchArea["y3"])
                            ]
                        )
                    )
                )
        except BaseException:
            return jsonify({'result': ['入力エラー']})

        # base64エンコードされたデータをデコードする
        pdfAllBinary: bytes = base64.b64decode(jsonData['uploadBase64'])
        pdfStrConvert: str = str(pdfAllBinary)

        if "b'data:application/pdf;base64," in pdfStrConvert:  # ヘッダーがあれば削除
            # ヘッダー削除
            deletedHeaderPdf = pdfStrConvert.replace("b'data:application/pdf;base64,", '').replace("EOF'", 'EOF')
            # バイト変換
            pdfBinaryReConverted = bytes(deletedHeaderPdf, encoding="utf-8")
            # ヘッダーを取り除いたところで再度base64デコード
            binaryPdf: bytes = base64.b64decode(pdfBinaryReConverted)
            imageProcess: ImageProcess = ImageProcess()
            # 画像データをGoogleVisionAPIのdetectDocumentで解析
            searchAreaTextList: List[str] = imageProcess.pickUpTextFromSearchAreas(binaryPdf, searchAreas)

            return jsonify({'result': searchAreaTextList})
        else:
            if "%PDF" in pdfStrConvert:  # ヘッダーがないPDFファイルであればそのまま渡す
                imageProcess: ImageProcess = ImageProcess()
                # 画像データをGoogleVisionAPIのdetectDocumentで解析
                searchAreaTextList: List[str] = imageProcess.pickUpTextFromSearchAreas(pdfAllBinary, searchAreas)
                return jsonify({'result': searchAreaTextList})
            else:  # PDFファイルでなければ終了
                return jsonify({'result': ['ファイルが正しくありません']})
