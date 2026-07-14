from flask import Blueprint , render_template , request , redirect, url_for , flash , session
from .models import users,User 

auth = Blueprint("auth",__name__)

@auth.route('/Login', methods=['GET','POST'])
def reading_tracker_login():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        #request username from HTML username ID and stores as username variable
        password = request.form.get('password','')
        #Requests password from HTML (login) , login ID and stores as password

        #Validating INPUTS
        if not username or not password:
            flash('please fill in all fields','Invalid Username or Password ERROR')
            return redirect(url_for('auth.reading_tracker_login'))
        #Authenitcation 
        if username in users and users[username].password == password:
            session['user']= username 
            flash('Login successful','success')
            if users[username].role == "teacher":
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard_home'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.reading_tracker_login'))
    #IF GET request render Login template
    return render_template('login.html')


@auth.route('/Register', methods =['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username',)
        password = request.form.get('password',)
        role = request.form.get('role')
        
        if not username or not password : 
            flash('Please fill in all fields',category='error')
            return render_template("register.html")
    
        if username in users:
            flash('Username already exists','error')
            return render_template("register.html")
    
        new_user = User(username, password ,role)
        users[username] = new_user
        flash('Account created successfully!',category='success')
        return redirect(url_for('auth.reading_tracker_login'))
    return render_template('register.html')#IF Request template render register template

@auth.route('/Logout')
def logout():
    session.pop('user',None)
    flash('You have been logged out successfully!')
    return redirect(url_for('auth.reading_tracker_login'))



