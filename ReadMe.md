# 線形計画法を利用した効率的なコマ組の構築
## 線形計画法の導入
```Python
# ライブラリのインポート
import pulp

# 線形計画問題の定義
problem = pulp.LpProblem('ProbremName', pulp.LpMaximize)
# 目的変数を最大化したい場合は、pulp.Maximize, 最小化したい場合は、pulp.Minimizeを利用する。

# 変数の定義
NewValue = pulp.LpVariable("NewValue",最小値, 最大値, 形式)
# 形式は、整数値の場合はIntegerを指定する(他にはfloat型連続値'Continuous'、2値変数'Binary'が指定できる)
```

# 線形問題の定義
1. 講習期間の定義   
    * 開始日: 2024/2/21
    * 終了日: 2024/3/31
2. 教務スタッフの情報を定義
    1. 教務スタッフのyyyy年mm月dd日のnコマ目の入室可否のデータを変数として定義
        ```Python
        teachername_PossTime_yyyymmddn = pulp.LpVariable("teachername_PossTime_yyyymmddn",0,1,"Integer")
        ```
    2. 教務スタッフの科目コードabcdeの授業実施可否についてのデータを定義
        ```Python
        teachername_PossSubject_abcde = pulp.LpVariable("teachername_PossSubject_abcde",0,1,"Integer")
        ```
    3. 教室の利用可能ブース数についての定義
        ```Python
        room_n_poss_yyyymmddn = pulp.LpVariable("room_n_poss_yyyymmddn",0,5,"Integer")
        ```
    4. 最大可能授業講師数
        該当時間における最大講師数の定義を行う。例えば、教室のブースが5つ空いている場合は、最大可能授業講師数は5になる。
        ```Python
        booth_num_yyyymmddn = pulp.LpVariable("booth_num_yyyymmddn",0,5,"Integer")
        ```