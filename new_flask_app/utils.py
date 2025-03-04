from datetime import datetime, timedelta
import sqlite3
import locale
from dx_app import db
from flask import current_app as app
from dx_app.models import Organization, Depertment, Period, Attention, Subject,Grade, Booth
from dx_app.models import User, Student, Educator, Guardian
from dx_app.models import SubjectPossib, ShiftPossib,ShiftSubmission, ShiftComp

from sqlalchemy import and_, or_


locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")


def add_record_to_table(table, data: dict):
    """
    指定されたテーブルにデータを追加する関数

    Args:
        table: データを追加するテーブルモデル
        data (dict): 追加するデータの辞書

    Returns:
        bool: 追加が成功したかどうか
    """
    try:
        record = table(**data)
        db.session.add(record)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"エラーが発生しました: {str(e)}")
        return False
    
def delete_record_from_table(table, id):
    """
    指定されたテーブルのレコードを削除する関数

    Args:
        table: データを削除するテーブルモデル
        id: 削除するレコードのID

    Returns:
        bool: 削除が成功したかどうか
    """
    try:
        record = table.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        db.session.rollback()
        print(f"エラーが発生しました: {str(e)}")
        return False
            


def make_dict(pagename,
              form=None,
              progress=None,
              datedata=False,
              period_data=False,
              shift_possib_data=False,
              grade_data=False,
              educator_list=False,
              student_list=False,
              organization_id = None,
              depertment_id = None,
              user_id_list = [],
              user_id = None
              ):
    '''
    引数で与えられたページ名に応じた辞書を返す
    pagename:str/pagenameのに応じたタイトルを返す
    form:formオブジェクト(formがある場合はformオブジェクトを返す)
    progress:progressオブジェクト(progressがある場合はprogressオブジェクトを返す)
    datedata:bool(日付データが必要である場合には返す)
    organization_id:int/所属団体ID(staff_listがある場合はstaff_listを返す)
    '''
    global staff_list,date_list,weekday_list
    # 初期設定
    dict={}
    period_list = ["1限", "2限", "3限", "4限", "5限"]

    # 各ページに応じた引渡しデータの編集
    dict["title"] = get_title(pagename)
    dict["form"] = form
    dict["progress"] = progress
    if datedata:
        dict["datedata"] = get_date_info()
    if period_data:
        dict["period_data"]=get_data_by_filting(table=Period,
                                           filters={"organization_id":organization_id,
                                                    "depertment_id":depertment_id,
                                                    }
                                                )
    if educator_list:
        dict["educator_list"]=get_data_by_filting(table=Educator,
                                               filters={"organization_id":organization_id,
                                                        "depertment_id":depertment_id,
                                                        }
                                               )
    if student_list:
        dict["student_list"]=get_data_by_filting(table=Student,
                                               filters={"organization_id":organization_id,
                                                        "depertment_id":depertment_id,
                                                        }
                                               )
    if shift_possib_data:
        dict["shift_possib_data"]=get_data_by_filting(table=ShiftPossib,
                                               filters={"user_id":user_id_list}
                                               )
    if grade_data:
        dict["grade_data"]=get_grade_data(organization_id, depertment_id)

    return dict


# 日付情報取得
def get_date_info():
    date_data = [(datetime.today()+timedelta(days=i)).date() for i in range(7)]
    month_list =[int(j) for j in  [i.strftime("%m") for i in date_data]]
    date_list=[int(j) for j in  [i.strftime("%d") for i in date_data]]
    month_date_list = [f"{month_list[i]}月{date_list[i]}日" for i in range(7)]
    weekday_list = [i.strftime("%a") for i in date_data]
    return {"date_data":date_data,
            "month_list": month_list,
            "date_list": date_list,
            "month_date_list": month_date_list,
            "weekday_list": weekday_list}

# タイトル取得
def get_title(pagename):
    titles={
        #auth
        "login":"ログイン",
        "register":"アカウントの作成",
        #dashboard
        "dashboard-student-cram":"塾生向けダッシュボード",
        "dashboard-student-individual":"個人学生向けダッシュボード",
        "dashboard-educator":"教室運営者向けダッシュボード",
        "guardian":"保護者向けダッシュボード",
        "edit-profile":"プロフィール編集",
        "chatbot":"教室運営用AIエージェント",
        "homepage":"ホーム",
        "shift-sub":"シフトの提出"
    }
    return titles[pagename] if pagename in titles else "タイトル情報が見つかりません"

# テーブルのフィルター取得
def get_data_by_filting(table=None, filters=None):
    """
    指定したテーブルのデータを複数の条件で取得（同じカラムの OR 条件にも対応）。

    :param table: SQLAlchemy モデル（例: User）
    :param filters: 条件の辞書（例: {"A": ["a", "b"], "B": "c"}）
    :return: データの辞書（成功: {"condit": True, "data": [...]}, 失敗: {"condit": False, "data": None}）
    """
    data = []
    try:
        with app.app_context():
            column_names = table.__table__.columns.keys()
            # 条件がない場合はすべてのデータを取得
            if not filters:
                records = table.query.all()
            else:
                filter_conditions = []
                # 条件を処理
                for col, val in filters.items():
                    if col in column_names and val is not None:
                        if isinstance(val, list):  # もしリストなら OR 条件
                            filter_conditions.append(or_(*[getattr(table, col) == v for v in val]))
                        else:  # 単一値なら AND 条件
                            filter_conditions.append(getattr(table, col) == val)
                # 条件がある場合のみ適用
                if filter_conditions:
                    records = table.query.filter(and_(*filter_conditions)).all()
                else:
                    records = table.query.all()
            # 結果を辞書のリストに変換
            for record in records:
                data.append({column_name: getattr(record, column_name) for column_name in column_names})
            if len(data)>0:
                return {"condit": True, "data": data}
            else:
                return {"condit": False, "data": None}
    except Exception as e:
        print(f"Error: {e}")  # デバッグ用
        return {"condit": False, "data": None}

def get_grade_data(organization_id, depertment_id):
    grade_list=get_data_by_filting(table=Grade,
                                    filters={"organization_id":organization_id,
                                            "depertment_id":depertment_id,
                                            }
                                    )
    if len(grade_list)>1:
        _ = []
        for i in range(len(grade_list)):
            _.append(grade_list[j] for j in range(len(grade_list)) if grade_list[j]["priority"] ==i )
        return _
    else:
        return grade_list