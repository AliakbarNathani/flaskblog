from flask import Flask,url_for, redirect, request,render_template
from flask_mysqldb import MySQL
app = Flask(__name__)
mysql = MySQL(app)

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    MYSQL_HOST='localhost',
    MYSQL_USER='root',
    MYSQL_PASSWORD='',
    MYSQL_DB='flaskblog'
))


"""Normal Routing"""
@app.route('/')
def hello_world():
    return 'Hello, World!'

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


"""HTTP request methods i.e get/post"""
@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method == 'GET'):
        return "show the login page"
    else:
        return "do the login"
    
"""Rendering Templates"""
@app.route('/render/<name>')
def render(name):
    return render_template('render.html',name=name)


@app.route('/getData')
def getData():
    cursor = mysql.connection.cursor();
    sql = "select *from posts"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('data.html',data=data)
        