# 本リポジトリについて
本リポジトリでは、個別指導塾におけるDXの一環として、教務スタッフのシフト提出からコマの割り振りまでのワークフロー改善を行いました。それにより、社員の割り振りプロセスの時間短縮やシフト調整の幅が格段に上昇しました。そのため、この事例をもとに多くの現場で導入できるように、本リポジトリを公開させていただきました。

# 開発環境について

本システムの開発に使用しているローカル環境は以下の通りです。   

> PC: Apple MacBook Air M1 2020モデル   
>利用ツール: `Visual Studio Code`, `Google Spread Sheet`, `Google Colaboratory`, `Line`   
>開発言語: `Python`   


# 問題要件定義について
本モデル

1. 教務スタッフの情報を定義
    1. 教務スタッフのyyyy年mm月dd日のnコマ目の入室可否のデータを変数として定義
        ```Python
        teachername_PossTime_yyyymmddn = pulp.LpVariable("teachername_PossTime_yyyymmddn",0,1,"Integer")
        ```
    2. 教務スタッフの科目コードabcdeの授業実施可否についてのデータを定義
        ```Python
        teachername_PossSubject_abcde = pulp.LpVariable("teachername_PossSubject_abcde",0,1,"Integer")
        ```
2. 環境因子の設定
    1. 教室の利用可能ブース数についての定義
        ```Python
        room_n_poss_yyyymmddn = pulp.LpVariable("room_n_poss_yyyymmddn",0,5,"Integer")
        ```
    2. 最大可能授業講師数
        該当時間における最大講師数の定義を行う。例えば、教室のブースが5つ空いている場合は、最大可能授業講師数は5になる。
        ```Python
        booth_num_yyyymmddn = pulp.LpVariable("booth_num_yyyymmddn",0,5,"Integer")
        ```
    3. 講習期間の定義   
        * 開始日: 2024/2/21
        * 終了日: 2024/3/31
        ```Python
        day_open_yyyymmddn = pulp.LpVariable("day_open_yyyymmddn",0,1,"Integer")
        ```
3. 生徒情報の定義
    生徒の来塾可能日程や履修科目やコマ数等について定義する。
    1. 来塾可能日程についての定義
    2. 履修科目の定義
    3. 残りコマ数の定義
    4. 主要な科目担当者の定義
    5. 生徒の情報(学年や性別等,NG講師等)の定義
    6. 備考
    