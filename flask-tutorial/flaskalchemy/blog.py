from flask import Flask,Blueprint, render_template,redirect,request,flash,url_for,abort,g,session
from flaskalchemy.db import Post, db, User
from flaskalchemy.auth import login_required
from sqlalchemy import desc
from . import Mail,Message,mail
bg = Blueprint('blog', __name__,template_folder='template')


@bg.route('/')
def index():
    """ view for show blog"""
    return redirect(url_for("blog.showblog"))

@bg.route('/<int:id>/read')
def read(id):
    error = None
    """ go() view for read post by id"""
    try:
        post = Post.query.filter_by(id=int(id)).first()
        return render_template('indexpost.html', Post=post)
    except Exception as e:
        print("If id not entered please enter id...........")




@bg.route('/add',methods=['GET','POST'])
def add():
    error=None
    """" add() view use for create new blog and publish it."""
    if request.method == 'POST':
        category=request.form['category']
        title=request.form['title']
        body=request.form['body']

        try:
            if not category or not title or not body :
                error='Please enter all the fields'
                flash(error)
            else:
                # for i in range(50):
                blog = Post(category,title,body, g.user.id)
                db.session.add(blog)
                db.session.commit()
                # msg = Message(str(blog.title),sender = 'prashantmali.info@gmail.com', recipients = [blog.user.username])
                # msg.body = str(blog.body)
                # mail.send(msg)
                print("send",".............")
                return redirect(url_for('blog.index'))
        except DatabaseError as de:
            print(de,"............database error")
        except Exception as e:
            print(e)

    return render_template('blog/create.html')

@bg.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()

    print(g.user,"............name")

@bg.route('/showblog')
def showblog():
    """ showblog() view write for display all post to user"""
    try:
        blog=Post.query.order_by(desc(Post.pub_date)).all()
        c = len(blog)
        return render_template('show_blog.html', blog=blog, user=g.user, c=str(c))
    except Exception as e:
        print("database not found")


@bg.route('/go',methods=('GET','POST'))
def go():
    error = None
    """ go() view for read post by id"""
    if request.method == 'POST':
        try:
            id = request.form['pid']
            if not id:
                error = 'Title is required.'
                flash(error)
            if error is not None:
                flash(error)
        except AttributeError as e:
            print("If id not entered please enter id...........")
        # except Exception as e:
        #     print("...........")
        else:
            post = Post.query.filter_by(id=id).first()
            print("...............",post.id,post.category)
            return render_template('indexpost.html',Post=post)

    

def get_post(id, check_author=True):
    post = Post.query.get(int(id))
    print(post.id)
    print(post.title)
    print(post.body)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    # users_post = User.query.filter(User.id == g.current_user.id).first()

    if check_author and post.a_id != g.user.id:
        abort(403)
    return post


@bg.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(int(id))
    print("................post",post.title)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title=title
            post.body=body
            db.session.add(post)
            db.session.commit()
            # msg = Message(str(post.title),sender = 'prashantmali.info@gmail.com', recipients = [post.user.username])  
            # msg.body = "Updated:"+"Title=>"+str(post.title)+"\n"+"Body=>"+ str(post.body) 
            # mail.send(msg)    
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)



@bg.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db.session.delete(get_post(id))
    db.session.commit()
    return redirect(url_for('blog.showblog'))

@bg.route('/<int:id>/sendemail')
@login_required
def sendemail(id):
    user=User.query.get(int(id))
    posts=Post.query.filter_by(a_id=user.id).first()
    msg = Message(str(posts.title), sender='prashantmali.info@gmail.com', recipients=[user.username])
    msg.body = posts.body
    mail.send(msg)
    return redirect(url_for('blog.index'))

