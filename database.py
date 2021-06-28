from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

"""FlaskアプリがSQLAlchemyを使えるようにするための初期化"""

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    Migrate(app, db)
