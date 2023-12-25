from flask import Flask, render_template
from db import connect

app = Flask(__name__)

@app.route("/") 
def index():

    db,c = connect()

    return render_template("index.html", page="home")

@app.route("/blogs")
def blogs():
    return render_template("blog.html", page="blog")

@app.route("/write", methods=['GET', 'POST'])
def write():
    return render_template("write.html", page="write")

if __name__ == '__main__':
    app.run()