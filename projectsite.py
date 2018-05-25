# coding: utf-8

import os
import flask

from flask import Flask, render_template, request
app = Flask(__name__)

from flask import abort, Blueprint
from flask.ext.bootstrap import Bootstrap

from config import config
from form_exec import *
from forms import *

import chartkick

bootstrap = Bootstrap(app)

# 
app.config.from_object(config[os.getenv("FLASK_CONFIG") or "default"])
ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/')
app.jinja_env.add_extension("chartkick.ext.charts")


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/aboutass")
def aboutass():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contactme.html")


@app.route("/crypt/<crypt_type>", methods=["GET", "POST"])
def crypt(crypt_type):
    crypt_forms = {
        "classic": ClassicCryptForm,
        "des": DESCryptForm,
        "rsa": RSACryptForm,
        "lfsr": LFSRCryptForm,
        "dsa": DSASignForm,
    }
    subtitles = {
        "classic": u"古典加密——仿射密码",
        "des": u"DES加密",
        "rsa": u"RSA加密",
        "lfsr": u"序列密码",
        "dsa": u"DSA数字签名",
    }

    if crypt_type not in subtitles:
        abort(404)

    form = (crypt_forms[crypt_type])()  # 对提交的表单进行处理（如加密）
    other_params = {}

    if request.method == "POST":
        if form.validate_on_submit():
            form, other_params = exec_form(crypt_type, form)
    elif crypt_type == "lfsr":
        form, other_params = exec_form(crypt_type, form)

    return render_template(crypt_type + "_crypt.html",
                           form=form,
                           subtitle=subtitles[crypt_type],
                           **other_params)


@app.route("/prime_test", methods=["POST"])
def prime_test():
    from cryptlib.RSA import is_prime
    try:
        number = int(request.form["number"])
        times = int(request.form["times"])
    except ValueError:
        abort(400)
    return str(is_prime(number, times))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def interbal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run('0.0.0.0')
