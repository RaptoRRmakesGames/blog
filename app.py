from flask import Flask, render_template, request, session, redirect, url_for, flash
from db import connect, get_blog, get_user, get_all_blogs,login, get_user_by_name, add_user, add_blog
from werkzeug.security import generate_password_hash, check_password_hash

from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'very secret yes'

Session(app)



@app.route("/") 
def index():
    db,c = connect()
    return render_template("index.html", page="home", session=session)

@app.route("/blogs")
def blogs():
    all_blogs = []
    for i,blog in enumerate(get_all_blogs()):
        all_blogs.append([blog[0], blog[1], blog[2], blog[3][0:24]+".."]) 
    return render_template("blog.html", page="blog", blogs=all_blogs, session=session)

@app.route("/blogs/<int:id>")
def see_blog(id):

    blognum = id

    blog = get_blog(blognum)
    user = get_user(blog[1])

    return render_template("see_blog.html", blog=blog, user=user)

@app.route("/write", methods=['GET', 'POST'])
def write():

    try:
        if not session['authenticated']:
            return redirect(url_for('login_page'))
    except Exception:
        return redirect(url_for('login_page'))
    
    if request.method == 'POST':
        add_blog(session["authenticated"], request.form["header"], request.form["textarea"])
        flash("Blog Posted Sucessfully!")
        return redirect(url_for("index"))



    return render_template("write.html", page="write", session=session)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    
    if request.method == 'POST':
        user,passw = request.form.get("username"),request.form.get("password")
        res = login(user,passw)
        flash(res)
        if res == "Login Successfull":
            session['authenticated'] = True
            session['id'] = get_user_by_name(user)[0]
            session["username"] = user
            return redirect(url_for('index'))

    return render_template("login.html", page="login", session=session)

@app.route("/register", methods=['GET', 'POST'])
def register():
     
    if request.method == 'POST':
        user,passw = request.form.get("username"),request.form.get("password")
        add_user(user, generate_password_hash(passw))

        res = login(user,passw)
        flash(f"Welcome to KafaBlogs, {user}")
        if res == "Login Successfull":
            session['authenticated'] = True
            session['id'] = get_user_by_name(user)[0]
            session["username"] = user
            return redirect(url_for('index'))
        

    return render_template("register.html", page="register", session=session)

@app.route("/logout")
def logout():
    session["authenticated"] = False
    session.pop("id")
    session.pop("username")
    flash("Sucessfully Logged Out!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()