from flask import Blueprint , render_template , request , redirect, url_for , flash , session
from .models import users,User 

home = Blueprint('home',__name__)

@home.route('/dashboard',)
def dashboard_home():
    
    if 'user' not in session:
        flash('Please log in first!','error')
        return redirect(url_for("auth.reading_tracker_login"))
    
    username = session['user']
    user = users.get(username)

    

    stats = user.viewStatistics()
    return render_template("dashboard.html",username=username,stats = stats )

@home.route('/readinglog', methods=['GET','POST'])
def log_reading():
    username = session.get("user")
    if not username:
        flash("You must be logged in to log reading session")
        return redirect(url_for("auth.reading_tracker_login"))
    
    user = users.get(username)

    if request.method == "POST":
        bookTitle = request.form['book_title']
        pagesRead = int(request.form["pages_read"])
        duration = int(request.form["duration"])

        user.addReadingLog(bookTitle,pagesRead,duration)
        flash("Reading session logged successfully!","success")
        return redirect(url_for("home.dashboard_home"))
    
    return render_template('log_reading.html')

@home.route("/history")
def history():
    username = session.get("user")
    if not username:
        return redirect(url_for("auth.reading_tracker_login"))
    
    user = users.get(username)
    return render_template("reading_history.html", logs = user.readingLogs,username=username)

@home.route("/leaderboard")
def leaderboard_page():
    username = session.get("user")
    if not username:
        flash("Please login to access the leaderboard.","error")
        return redirect(url_for("auth.reading_tracker_login"))
    
    from .models import generate_leaderboard_data 
    data = generate_leaderboard_data()

    sorted_data = sorted(data, key=lambda x:x["pages"],reverse=True)

    return render_template("leaderboard.html",leaderboard = sorted_data)
    
