from flask import Blueprint, render_template, request, jsonify, redirect, url_for

bp = Blueprint("student", __name__)

students = [
    {"id": 1, "name": "田中 太郎", "grade": "中学生", "teacher": "佐藤先生", "subject": "数学", "status": "在籍"},
    {"id": 2, "name": "鈴木 花子", "grade": "高校生", "teacher": "山本先生", "subject": "英語", "status": "休会"},
    {"id": 3, "name": "山田 次郎", "grade": "小学生", "teacher": "高橋先生", "subject": "理科", "status": "在籍"},
]


@bp.route("/")
def manage_student():
    teachers = list(set([s["teacher"] for s in students]))
    return render_template("dx_app/manage-student.html", data={"students": students, "teachers": teachers})

@bp.route("/<int:student_id>")
def student_detail(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return "生徒が見つかりません", 404
    return render_template("dx_app/student-detail.html", student=student)

@bp.route("/<int:student_id>/update", methods=["POST"])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return "生徒が見つかりません", 404

    student["name"] = request.form["name"]
    student["grade"] = request.form["grade"]
    student["teacher"] = request.form["teacher"]
    student["subject"] = request.form["subject"]
    student["status"] = request.form["status"]

    return redirect(url_for("student.manage_student"))

@bp.route("/filter-students", methods=["POST"])
def filter_students():
    data = request.get_json()
    filtered_students = [s for s in students if
                         (not data["grade"] or s["grade"] == data["grade"]) and
                         (not data["subject"] or s["subject"] == data["subject"]) and
                         (not data["teacher"] or s["teacher"] == data["teacher"]) and
                         (not data["status"] or s["status"] == data["status"])]

    return jsonify({"students": filtered_students})



