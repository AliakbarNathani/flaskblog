from flask import Flask,url_for, redirect, request,render_template,flash,session
from flask_login import *
from werkzeug.security import generate_password_hash,check_password_hash
from models2 import *
import traceback,pickle

app = Flask(__name__)
app.secret_key = 'flaskblog12345'

app.config['LOGIN_DISABLED'] = False
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.get(User.id)


"""Registration Module using models"""
@app.route('/register',methods=['GET','POST'])
def register():
    if(request.method == 'GET'):
        return render_template('register.html')
    else:
        user = User.create(name=request.form['name'],email=request.form['email'],password=generate_password_hash(request.form['password'],method='sha256'))
        flash('User Registered successfully')
        return redirect(url_for('home'))


"""Login Module using flask-login"""
@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method == 'GET'):
        if not current_user.is_authenticated:
            return render_template('login.html')
        else:
            return redirect(url_for('home'))
    else:
        user = User.get(User.email==request.form['email'])

        if(check_password_hash(user.password,request.form['password'])):
            login_user(user)
            flash('Login successful')
            return redirect(url_for("home"))
        return render_template('login.html')

"""Login module using flask-logout"""
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

"""Add post module using Posts model"""
@app.route('/addPost',methods=['GET','POST'])
@login_required
def addPost():
    if(request.method == 'GET'):
        return render_template('createPost.html')
    else:
        Posts.create(user_id=current_user.id,title=request.form['title'],body=request.form['body'])
        flash('Post created successfully')
        return redirect(url_for('home'))

"""Route for home page displaying all the posts"""
@app.route('/')
@login_required
def home():
    posts = Posts.select()
    return render_template('index.html',data=posts)


"""Route for profile where only user's post is shown"""
@app.route('/profile')
@login_required
def profile():
    posts = Posts.select().where(Posts.user_id == current_user.id)
    return render_template('profile.html',data=posts)

@app.route('/test')
def test():
    return str(session['user_id'])
"""Enables Debugging in python """
if __name__ == '__main__':
    app.run(debug=True)
