from flask import Flask
from flaskalchemy.db import db
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///updateblog.db'
    app.config['SECRET_KEY'] = 'dev'

    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.abp)

    from . import demoblueprint
    app.register_blueprint(demoblueprint.dbp)

    from . import blog
    app.register_blueprint(blog.bg)
    app.add_url_rule('/', endpoint='index')
    return app


if __name__=='__main__':
    db.create_all()