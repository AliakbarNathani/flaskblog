from flask import Flask,url_for, redirect, request,render_template,flash,session
from flask_login import login_required, current_user,LoginManager
from models import *

app = Flask(__name__)
app.secret_key = 'flaskblog12345'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


"""Normal Routing"""
@app.route('/')
def home():
    return 'home page'

@app.route('/hello')
def hello():
    return 'Hello, Python!'


"""We can pass arguments to a route
and also we can override the routes according to the data type of parameters"""

@app.route('/user/<id>')
def getID(id):
    return 'Username is %s' % id

@app.route('/user/<int:id>')
def show_user_profile(id):
    # show the user profile for that user
    return 'User id %d' % id


"""Accessing '/projects/' route without trailing slash would not give any error"""
@app.route('/projects/')
def projects():
    return 'The project page'

"""Accessing '/about' route without trailing slash would give 404 error"""
@app.route('/about')
def about():
    return 'The about page'

"""url_for(method_name,parameters) returns the url for the method specified and pass parameters to it"""
@app.route('/redirect')
def redit():
    return redirect(url_for('getID',id='1'))

"""Rendering Templates"""
@app.route('/render/<name>')
def render(name):
    return render_template('render.html',name=name)


"""Mysql connection,querying and rendering it to an html page"""
@app.route('/getData')
def getData():
    #Getting posts related to the user
    user     = User.get(id=session['id'])
    allposts = user.posts
    return render_template('data.html',data=allposts,name=user.name)

"""Getting all posts"""
@app.route('/getAllPosts')
@login_required
def getAllPosts():
    #Getting posts related to the user
    users    = User.select()
    allposts = Posts.select()
    return render_template('data.html',data=allposts)


"""Add Post"""
@app.route('/addPost',methods=['GET','POST'])
@login_required
def addPost():
    if(request.method == 'GET'):
        if not session.get('id'):
            return redirect(url_for('login'))
        else:
            return render_template('createPost.html')
    else:
        Posts.create(user=session['id'],title=request.form['title'],body=request.form['body'])
        flash("New Entry was successfully added")
        return redirect(url_for('getData'))


"""registration of users"""
@app.route('/register',methods=['GET','POST'])
def register():
    if(request.method == 'GET'):
        return render_template('register.html')
    else:
        user = User.create(name=request.form['name'],email=request.form['email'],password=request.form['password'])
        session['id'] = user.id
        flash("Registration successful Please login to continue")
        return redirect(url_for('login'))


"""login with session handling"""
@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method == 'GET'):
        if not session.get('id'):
            return render_template('login.html')
        else:
            return redirect(url_for('home'))
    else:
        try:
            user = User.get(User.email==request.form['email'],User.password == request.form['password'])
            session['id'] = user.id
            return redirect(url_for('home'))
        except User.DoesNotExist:
            return redirect(url_for('login'))


"""logout session destroying"""
@app.route('/logout')
@login_required
def logout():
    session.pop('id')
    return redirect(url_for('login'))

"""Enables Debugging in python """
if __name__ == '__main__':
    app.run(debug=True)
