import os
import datetime as datetime
import re


class OtherService():

    def removeOldFile(self):
        """ 古い画像ファイルを削除する
        """
        # １日前のファイルを削除する
        # img/tmpにあるファイル一覧を取得
        tmpImagePath: str = "assets/img/tmp/"
        files = os.listdir(tmpImagePath)
        for fileName in files:
            # 日付の文字列を取得
            result = re.match('^img_(\\d\\d\\d\\d\\d\\d\\d\\d)_.*$', fileName)
            if result:
                fileCreateDate = datetime.strptime(result.group(1), '%Y%m%d')
                today = datetime.strptime(str(datetime.now().year) +
                                          str(datetime.now().month) +
                                          str(datetime.now().day), '%Y%m%d')
                # 今日より前であれば削除する
                if fileCreateDate < today:
                    os.remove(tmpImagePath + fileName)
