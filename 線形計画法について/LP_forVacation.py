import pulp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np
import datetime as dt
from tqdm import tqdm
from IPython.display import display
from tqdm imort tqdm


def LP_makeTestData():
    start = dt.datetime(2025, 2, 14)
    finish = dt.datetime(2025, 3, 1)
    # 教務スタッフの生成
    teacher_list = [f"教師{i}" for i in range(16)]
    # 生徒の作成
    student_list = [f"生徒{i}" for i in range(61)]
    # 科目の作成
    subject_list = [f"科目{i}" for i in range(26)]
    teacher_sub_dict = {}
    for i in range(len(teacher_list)):
        sub_avi_list = []
        for j in range(len(subject_list)):
            n = random.randint(0,1)
            sub_avi_list.append(n)
        teacher_sub_dict[teacher_list[i]] = sub_avi_list
    df_teacher = pd.DataFrame(teacher_sub_dict,index=subject_list).T
    print("教務スタッフ指導可能科目について")
    display(df_teacher)
    student_sub_dict = {}
    for i in range(len(student_list)) :
        sub_avi_list = []
        while 1 not in sub_avi_list:
            sub_avi_list = np.random.choice([0, 1], size=len(subject_list), p=[0.96, 0.04])
        student_sub_dict[student_list[i]] = sub_avi_list
    df_student = pd.DataFrame(student_sub_dict,index=subject_list).T
    print("生徒受講科目設定")
    display(df_student)
    all_num=0
    for i in student_list:
        all_num+=len(df_student.T[df_student.T[i]==1].index)
    print(all_num)
    # 日付リストの設定
    date_list = pd.date_range(start=start, end=finish)
    avi_time_dict={}
    for day in date_list:
        avi_time = [0 for i in range(7)]
        if day.weekday()>=6:
            for time in range(0,7):
                avi_time[time]=1
        elif day.weekday() >=5:
            for time in range(1,7):
                avi_time[time]=1
        else:
            for time in range(2,7):
                avi_time[time]=1
        avi_time_dict[day.strftime("%m/%d/%a")]= avi_time
    print("指導可能授業時間について")
    display(avi_time_dict)
    # 日付リストの設定
    # 教師の予定を立てる
    date_list = pd.date_range(start=start, end=finish)
    teacher_avi_time_dict={}
    for teacher in teacher_list:
        avi_time_dict_={}
        for day in date_list:
            avi_time = []
            while sum(avi_time)==0:
                avi_time = np.random.choice([0, 1], size=7, p=[0.2, 0.8]).tolist()
            avi_time_dict_[day.strftime("%m/%d/%a")]=avi_time
        teacher_avi_time_dict[teacher]=avi_time_dict_

    # 生徒の予定を立てる
    student_avi_time_dict={}
    for student in student_list:
        avi_time_dict_={}
        for day in date_list:
            avi_time = []
            while sum(avi_time)==0:
                avi_time = np.random.choice([0, 1], size=7, p=[0.4, 0.6]).tolist()
            avi_time_dict_[day.strftime("%m/%d/%a")]=avi_time
        student_avi_time_dict[student]=avi_time_dict_
    print("生徒来塾可能日について")
    display(student_avi_time_dict)
    print("講師出勤可能時間について")
    display(teacher_avi_time_dict)
    #生徒と教師の紐付け
    list_st_te_sub =[]
    for subject in subject_list:
        student_get = df_student[df_student[subject]==1].index
        teacher_get = df_teacher[df_teacher[subject]==1].index
        for student in student_get:
            for teacher in teacher_get:
                # 生徒と教師と科目のセット変数が確定した(911コ)
                for day,avi_list_per_day in avi_time_dict.items():
                    for index,k in enumerate(avi_list_per_day):
                        #print(f"{i}日{index}限を開講しています")
                        #指導可能日のみ抽出済み
                        if k==1 and student_avi_time_dict[student][day][index] ==1 and teacher_avi_time_dict[teacher][day][index] ==1:    
                            for booth in ["AB","CD","EF","GH","IJ"]:
                                # この段階で、生徒-教務スタッフ-科目-日付-時限-ブースが確定した。
                                list_st_te_sub.append(f"{student}-{teacher}-{subject}-{day}日{index}限-{booth}")
                                print(f"{student}-{teacher}-{subject}-{day}日{index}限-{booth}")
    print("紐付き数",len(list_st_te_sub))
    
    
def SolveLinearProblem(teacher_list,
                       df_teacher,
                       student_list,
                       df_student,
                       List,
                       date_list):
    # 問題の定義
    prob = pulp.LpProblem('LP_class_Vacatrion', pulp.LpMinimize)
    # 変数を辞書化する
    x = pulp.LpVariable.dicts("x", List ,cat="Binary")
    # 教務スタッフについての制約条件
    for teacher in tqdm(teacher_list):
        for day in date_list:
            for index in range(7):
                day_ = day.strftime("%m/%d/%a")
                str = f"{day_}日{index}限"
                #print(str)
                for_teacher = [i for i in List if (f"-{teacher}-" in i and str in i)]
                if len(for_teacher)>1:
                    #print(f"{teacher}における{day}の{index}限で{for_teacher}")
                    #print(len(for_teacher),for_teacher)
                    prob += pulp.lpSum(x[t] for t in for_teacher) <= 2

    for student in tqdm(student_list):
        for day in date_list:
            for index in range(7):
                day_ = day.strftime("%m/%d/%a")
                str = f"{day_}日{index}限"
                #print(str)
                for_student = [i for i in List if (f"{student}-" in i and str in i)]
                if len(for_student)>1:
                    #print(f"{student}における{day}の{index}限で{for_student}")
                    #print(len(for_teacher),for_teacher)
                    prob += pulp.lpSum(x[t] for t in for_student) <= 1

    for day in tqdm(date_list):
        for index in range(7):
            day_ = day.strftime("%m/%d/%a")
            str = f"{day_}日{index}限"
            #print(str)
            for booth in ["AB","CD","EF","GH","IJ"]:
                for_booth_num = [i for i in List if (str in i) and booth in i]
                if len(for_booth_num)>1:
                    #print(f"{str}限{booth}で{for_booth_num}")
                    #print(len(for_teacher),for_teacher)
                    prob += pulp.lpSum(x[t] for t in for_booth_num) <= 2

    # 生徒の受講しているコマを入れ込む
    for student in tqdm(student_list):
        for subject in df_student.T[df_student.T[student]==1].index:
            for_st_sub_num = [i for i in List if (f"{student}-" in i) and (f"{subject}-" in i)]
            prob += pulp.lpSum(x[t] for t in for_st_sub_num) == 4

    for teacher in tqdm(teacher_list):
        for_teacher_low = [i for i in List if teacher in i]
        prob += pulp.lpSum(x[t] for t in for_teacher_low) <= 320

    # 目的変数としては、ブース稼働数最小限
    #ブース稼働数を変数とする必要がある。
    #例: 生徒53-教師0-科目0-02/14/Fri日5限-AB
    prob += pulp.lpSum(x[t] for t in [i for i in List if any(f"{index}限" in i for index in range(5))])
    prob.solve()
    list_answer = {}
    for v in prob.variables():
        print(v.name, "=", v.varValue)
        if v.varValue != 0:
            list_answer[v.name]=v.varValue
    class_complete = {}
    for student in student_list:
        class_complete[student]= [data for data in list_answer if f"{student}_" in data]

if __name__ == "__main__":
    LP_makeTestData()
    #SolveLinearProblem