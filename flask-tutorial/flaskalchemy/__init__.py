from flaskalchemy.db import db
from flask_mail import Mail, Message
from flask import Flask
from flask_migrate import Migrate
mail=Mail()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SECRET_KEY'] = 'dev'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'thdjkddjj.info@gmail.com'
    app.config['MAIL_PASSWORD'] = "suskdjdkkdjdj"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)
    db.init_app(app)
    mg = Migrate(db,app)
    mg.init_app(app)
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
    app.run()
