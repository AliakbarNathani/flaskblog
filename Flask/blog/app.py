from flask import Flask,url_for, redirect, request,render_template,flash,session
from models import *

app = Flask(__name__)
app.secret_key = 'flaskblog12345'


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
    allposts = Posts.select().where(Posts.user_id==session['id'])
#    return str(allposts)
    return render_template('data.html',data=allposts)


"""Add Post"""
@app.route('/addPost',methods=['GET','POST'])
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
def logout():
    session.pop('id')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)