from flask import Blueprint

dp = Blueprint('demo',__name__,url_prefix="/demo")


@dp.route("/demo")
def demo():
    return "this is demo blueprint"

@dp.route("/data")
def data():
    return "this is data blueprint"
