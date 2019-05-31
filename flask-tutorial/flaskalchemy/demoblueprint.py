from flask import Blueprint,render_template

dbp=Blueprint('demo',__name__)


@dbp.route('/demo')
def demo():
    return render_template('auth/add.html')
