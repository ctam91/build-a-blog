from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#create a Blog class with id, title, and body properties
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(800))

    def __init__(self, title, body):
        self.title = title
        self.body = body 

#create /newpost route and renders add template. If user leaves title or body blank, then return errors. 
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        title_error = ""
        body_error = ""

        if title == "": 
            title_error = "Please fill in the title"
            body = ""

        if body == "":
            body_error = "Please fill in the body"
            title = ""
            
        if not title_error and not body_error:   
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            blog_id = str(new_post.id) #grab the id for the record you just created
            return redirect('/blog?id='+blog_id)
        else: 
            return render_template('add.html', title_error=title_error, body_error=body_error, title=title, body=body)
        
    return render_template('add.html')

#create /blog route to display blog
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    #since this is a get request, use request.args.get to retrieve id of blog post
    blog_id = request.args.get('id')

    #if blog_id exists, send your db a query and find the post associated with that id. Render post.html with that post's title and blog
    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("post.html", title=post.title, body=post.body)
    
# If there are no specific posts, show entire blog. 
    titles = Blog.query.all()
    return render_template('blog.html',titles=titles)

@app.route('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()