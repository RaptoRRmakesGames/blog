from flask import Flask, render_template
from db import connect, get_blog, get_user, get_all_blogs

app = Flask(__name__)

@app.route("/") 
def index():
    db,c = connect()
    return render_template("index.html", page="home")

@app.route("/blogs")
def blogs():
    all_blogs = []
    for i,blog in enumerate(get_all_blogs()):
        all_blogs.append([blog[0], blog[1], blog[2], blog[3][0:24]+".."]) 
    return render_template("blog.html", page="blog", blogs=all_blogs)

@app.route("/blogs/<int:id>")
def see_blog(id):

    blognum = id

    blog = get_blog(blognum)
    user = get_user(blog[1])

    return render_template("see_blog.html", blog=blog, user=user)

@app.route("/write", methods=['GET', 'POST'])
def write():
    return render_template("write.html", page="write")

if __name__ == '__main__':
    app.run()