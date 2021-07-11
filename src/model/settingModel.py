import datetime
from database import db


class Setting(db.Model):

    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 設定名
    setting_name = db.Column(db.String(255), nullable=False)
    # 設定値
    setting_value = db.Column(db.String(255), nullable=False)
    # 作成日
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    # 更新日
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __init__(self, setting_name, setting_value):
        self.setting_name = setting_name
        self.setting_value = setting_value

    @staticmethod
    def isAvailableApi() -> bool:
        """ 使用回数が上限に達していなければ使用可(True)
        """
        # 本日の使用回数
        todayUsingNum: int = int(Setting.query.filter_by(setting_name="TodayUsingNum").first().setting_value)
        # 最終更新日
        lastUpdate: datetime = Setting.query.filter_by(setting_name="TodayUsingNum").first().updated_at
        # 1日あたりの上限回数
        maxDailyUsingNum: int = int(Setting.query.filter_by(setting_name="MaxDailyUsingNum").first().setting_value)

        judge: bool = False
        # 前回のDB更新日と今日の日付を比較
        if datetime.datetime.strptime(lastUpdate.strftime('%Y/%m/%d'), '%Y/%m/%d') \
                < datetime.datetime.strptime(datetime.datetime.now().strftime('%Y/%m/%d'), '%Y/%m/%d'):
            # 本日の使用回数をリセットする
            todayUsingNumData: Setting = db.session.query(Setting).filter_by(setting_name='TodayUsingNum').first()
            todayUsingNum = 0
            todayUsingNumData.setting_value = str(todayUsingNum)
            db.session.add(todayUsingNumData)
            db.session.commit()
        if todayUsingNum >= maxDailyUsingNum:
            judge = False
        else:
            # 本日の使用回数を1増やす
            todayUsingNumData: Setting = db.session.query(Setting).filter_by(setting_name='TodayUsingNum').first()
            todayUsingNumData.setting_value = str(todayUsingNum + 1)
            db.session.add(todayUsingNumData)
            db.session.commit()
            judge = True
        return judge
