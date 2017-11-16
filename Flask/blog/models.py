from peewee import *

mysql = MySQLDatabase(host='localhost',user="root",password="",database="fblog2")

"""Creating BaseModel with meta is database which will be used by all models"""
class BaseModel(Model):
    class Meta:
        database = mysql

"""Model for table user"""
class User(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    email = CharField(unique='true')
    password = CharField()

"""Model for table posts"""
class Posts(BaseModel):
    post_id = PrimaryKeyField()
    user = ForeignKeyField(User,related_name='posts')
    title=CharField()
    body = CharField()

def init_connect():
    mysql.connect()

    #This will create tables related to models
    mysql.create_tables([User,Posts],safe=True)

init_connect()
