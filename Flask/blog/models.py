from peewee import *

mysql = MySQLDatabase(host='localhost',user="root",password="",database="fblog")

class BaseModel(Model):
    class Meta:
        database = mysql
        

class User(BaseModel):
    id = PrimaryKeyField()	
    name = CharField()
    email = CharField(unique='true')
    password = CharField()
    
class Posts(BaseModel):
    post_id = PrimaryKeyField()
    user = ForeignKeyField(User)
    title=CharField()
    body = CharField()
    
def init_connect():
    mysql.connect()
    mysql.create_tables([User,Posts],safe=True)
    
init_connect()
