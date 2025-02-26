
def make_dict(pagename, form=None, progress=None):
    '''
    引数で与えられたページ名に応じた辞書を返す
    dict={title:"ページタイトル"}
    '''
    global staff_list,date_list, period_list,weekday_list
    # 初期設定
    dict={}
    titles={
        "login":"ログイン",
        "register":"アカウントの新規作成",
        "dashboard":"ダッシュボード",
        "edit-profile":"プロフィール編集",
        "chatbot":"教室運営用AIエージェント",
        "homepage":"ホーム",
        "shift-sub":"シフトの提出"
    }
    # 各ページに応じた引渡しデータの編集
    try:
        dict["title"] = titles[pagename]
    except:
        dict["title"] = "ページが見つかりません"
    try:
        dict["form"] = form
    except:
        dict["form"] = None
    try:
        dict["progress"] = progress
    except:
        dict["progress"] = None
    try:
        dict["data"]=[staff_list,date_list, period_list,weekday_list]
    except:
        dict["data"] = "データが取得できませんでした"
    return dict

