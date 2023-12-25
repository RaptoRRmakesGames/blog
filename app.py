from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", page="home")

@app.route("/blogs")
def blogs():
    return render_template("blog.html", page="blog")

@app.route("/write")
def write():
    return render_template("write.html", page="write")


app.run()