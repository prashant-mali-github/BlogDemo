from flask import Blueprint,request, flash, url_for, redirect, render_template,g,current_app,session
from flaskalchemy.db import User, db,Post
from werkzeug.security import check_password_hash
from sqlalchemy import desc
import functools

abp = Blueprint('auth', __name__, template_folder='template')

@abp.route('/show')
def show():
    users = User.query.all()
    # db.session.query(User).delete()
    # db.session.commit()
    return render_template('show_user.html', users=users)


@abp.route('/pagination')
def pagination():
    blog = Post.query.order_by(desc(Post.pub_date)).all()
    print(len(blog),"...........")
    return render_template('pagination.html', blog=blog, user=g.user)


@abp.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        error=None
        username = request.form['username']
        password = request.form['password']
        c_password=request.form['confirm_password']

        if password == c_password:
            user=User.query.filter_by(username=username).first()
            if not user:
                register = User(username=username, password=password)
                db.session.add(register)
                db.session.commit()
            else:
                error="Username already exist"
                flash(error)
                # error=""
                # flash(error)
            return redirect(url_for("auth.login"))
        else:
            error="Password and confirm password not match"
            flash(error)
    return render_template("auth/add.html")


@abp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        error = None
        uname = request.form["username"]
        passw = request.form["password"]

        user = User.query.filter_by(username=uname).first()
        if user and check_password_hash(user.password,passw):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('blog.showblog'))
        else:
            error = "Please enter valid credential"
            flash(error)
    return render_template("auth/login.html")

@abp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@abp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.showblog'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
