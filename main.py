from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(800))

    def __init__(self, title, body):
        self.title = title
        self.body = body 

@app.route('/newpost', methods=['POST', 'GET'])
def add_post():
 
    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        new_title = Blog(title_name, body_name)
        db.session.add(new_title)
        db.session.commit()

    titles = Blog.query.all()
    return render_template('add.html', titles=titles)



@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        new_title = Blog(title_name, body_name)
        db.session.add(new_title)
        db.session.commit()

    titles = Blog.query.all()
    return render_template('blog.html', titles=titles)


if __name__ == '__main__':
    app.run()