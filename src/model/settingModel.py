from datetime import datetime
from database import db


class Setting(db.Model):

    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 設定名
    setting_name = db.Column(db.String(255), nullable=False)
    # 設定値
    setting_value = db.Column(db.String(255), nullable=False)
    # 作成日
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # 更新日
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, setting_name, setting_value):
        self.setting_name = setting_name
        self.setting_value = setting_value
