import json
import os

import pymysql.cursors

"""初期データを入れる"""

# DB初期設定
con = pymysql.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    db=os.getenv('MYSQL_DATABASE'),
    charset='utf8'
)

# 作成・更新日付のデフォルト値を設定
con.cursor().execute('alter table settings ' +
                     'change column created_at created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,' +
                     'change column updated_at updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')

# ファイルを読み込む
json_open = open('fixtures/settingsData.json', 'r')
json_load = json.load(json_open)
#  データを入れる
for data in json_load:
    print(data)
    query = 'insert into settings(setting_name, setting_value) values(%s, %s)'
    con.cursor().execute(query, (data['setting_name'], data['setting_value']))
con.commit()
con.close()
# allUser = User.query.all()
# user: User = allUser[0]
# return user.name
