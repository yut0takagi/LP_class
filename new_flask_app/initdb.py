import sqlite3
from sqlalchemy import text
from dx_app import db
from wsgi import app

def init_db():
    with app.app_context():
        db.session.execute(text("PRAGMA foreign_keys=OFF;"))
        for table in db.metadata.sorted_tables:
            db.session.execute(text(f"DROP TABLE IF EXISTS {table.name};"))
            print(f"{table.name} を削除しました。")
        db.session.execute(text("PRAGMA foreign_keys=ON;"))
        db.create_all()
        print("SQLite の全テーブルを再作成しました。")
        db.session.commit()


if __name__ == "__main__":
    init_db()