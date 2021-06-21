import os
from flask import make_response


class ExcelProcess:
    """ Excel処理関係
    """

    # def __init__(self):

    def getResponse():
        """ レスポンスを作成する
        """
        # 出力Excelファイルのパス
        outputExcelFileName = "sample.xlsx"
        outputExcelFilePath = "secret/" + outputExcelFileName
        # Flaskのレスポンスを作成する
        response = make_response()
        # ダウンロードするEXCELファイルを開く
        wb = open(outputExcelFilePath, "rb")
        # ダウンロードするEXCELファイルをレスポンスに設定する
        response.data = wb.read()
        # ダウンロードするEXCELファイルをクローズ
        wb.close()
        # ダウンロードするEXCELファイル名を設定
        response.headers["Content-Disposition"] = "attachment; filename=" + outputExcelFileName
        # MIMEタイプをレスポンスに設定
        response.mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        # MIMEタイプをレスポンスに設定
        os.remove(outputExcelFilePath)
        return response
