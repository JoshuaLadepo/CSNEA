from flask import Blueprint, render_template, session, redirect, url_for, flash ,request
from .models import users

admin = Blueprint("admin",__name__)

@admin.route("/admin")
def admin_dashboard():
    username = session.get("user")
    if not username:
        return redirect(url_for("auth.reading_tracker_login"))
    
    current_user = users.get(username)

    if current_user.role != "teacher":
        flash("Access Denied","error")
        return redirect(url_for("home.dashboard_home"))
    
    students = [user for user in users.values() if user.role== "student"]

    return render_template("admin_dashboard.html",students = students)

@admin.route("/admin/student/<username>")
def view_student_logs(username):
    admin_user = session.get("user")

    if not admin_user or users[admin_user].role != "teacher":
        flash("Access denied")
        return redirect(url_for("home.dashboard_home"))

    student = users.get(username)

    if not student:
        flash("Student not found")
        return redirect(url_for("admin.admin_dashboard"))

    sort_by = request.args.get("sort", "date")
    logs = student.readingLogs.copy()

    if sort_by == "pages":
        logs.sort(key=lambda log: log.pages_read, reverse=True)
    elif sort_by == "duration":
        logs.sort(key=lambda log: log.duration, reverse=True)
    else:
        # default = date (newest first)
        logs.sort(key=lambda log: log.date, reverse=True)



    stats = student.viewStatistics()

    return render_template(
        "admin_student_logs.html",
        student=student,
        logs=logs,
        stats=stats,
        sort_by = sort_by
    )

@admin.route("/admin/student/<username>/delete/<int:index>", methods=["POST"])
def delete_student_log(username, index):
    admin_user = session.get("user")

    if not admin_user or users[admin_user].role != "teacher":
        flash("Access denied")
        return redirect(url_for("home.dashboard_home"))

    student = users.get(username)

    if student and 0 <= index < len(student.readingLogs):
        student.readingLogs.pop(index)
        flash("Reading log deleted successfully", "success")

    return redirect(url_for("admin.view_student_logs", username=username))
