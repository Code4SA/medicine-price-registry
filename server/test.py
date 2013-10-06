from flask import Flask
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(120))
    text = db.Column(db.UnicodeText, nullable=False)


admin = Admin(app)
admin.add_view(MyView(name="Hello"))
admin.add_view(ModelView(Post, db.session))

app.run()
