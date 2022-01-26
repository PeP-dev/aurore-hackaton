import os
from typing import final
import uuid
from datetime import timedelta, datetime
from functools import wraps

import jwt
from flask import request, render_template, make_response, redirect, url_for

from werkzeug.security import generate_password_hash, check_password_hash

from AuroreApp import app
from AuroreApp.mailing_service import MailgunMailingService, Mail
from AuroreApp.offres_service import MockOffreService
from AuroreApp.user_service import MockUserService, User

user_service = MockUserService()
offres_service = MockOffreService()
mailing_service = MailgunMailingService(os.getenv('MAILGUN_API_KEY'), os.getenv('MAILGUN_DOMAIN'))
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')


# decorator for verifying the JWT
@app.before_request
def check_auth():
    # jwt is passed in the request header
    token = request.cookies.get('aurore_login')
    request.current_user = None
    # return 401 if token is not passed
    if token:
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.current_user = user_service.get_user_by_id(data['public_id'])
        except:
            pass


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.current_user is None:
            return redirect(url_for('login', next=f.__name__))
        return f(*args, **kwargs)

    return decorated


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.current_user is None:
            return redirect(url_for('login', next=f.__name__))

        if not request.current_user.is_admin:
            return redirect(url_for(login), next=f.__name__)
        return f(*args, **kwargs)

    return decorated


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")


@app.route("/pro", methods=["GET"])
def pro_form():
    return render_template("pro.html")


@app.route("/pro", methods=["POST"])
def pro():
    data = request.form
    entreprise = data.get("entreprise")
    mail = Mail(["vautier.paul14350@gmail.com"], "Demande de contact Entr'ACT : {name}".format(name=str(entreprise)),
                "Ceci est un mail automatique envoyé par l'API Entr'ACT, L'entreprise {name} a effectué une demande de contact.\nContact :\n Mail : {mail}\nTéléphone : {tel}".format(
                    name=entreprise,
                    mail=data.get("email"),
                    tel=data.get("telephone", default="non fourni")
                ))
    print(mailing_service.send_mail(mail))
    return render_template("thanks.html")


@app.route("/particulier", methods=["GET", "POST"])
@require_auth
def particulier():
    # GET
    if request.method == "GET":
        return render_template("particulier.html")
    # POST
    elif request.method == "POST":
        form = request.form
        user = request.current_user

        try:
            _telephone = form.get('telephone')
        except KeyError as ke:
            _telephone = None

        return render_template("thanks.html")


@app.route("/account", methods=["GET"])
@require_auth
def account():
    return make_response(render_template('account.html'), 401)


# signup route
@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    email = data.get('email')
    password = str(data.get('password'))
    if not data.get('particulier'):
        return make_response(
            render_template('signup.html', error="La création de compte est réservée aux particuliers"))

    if not data:
        # returns 401 if any email or / and password is missing
        return make_response(render_template('signup.html', error="Formulaire invalide"),
                             401)

    if not data.get('email'):
        return make_response(
            render_template('signup.html', error="Merci de renseigner le champ email"), 400)

    if not password:
        return make_response(
            render_template('signup.html', error="Merci de renseigner le mort de passe"),
            400)

    # checking for existing user
    user = user_service.get_user_by_email(email)

    if not user:
        new_user = User(str(uuid.uuid4()), "", email, generate_password_hash(password), is_admin=True)
        user_service.add_user(new_user)
        return make_response(render_template('login.html'), 201)
    else:
        # returns 202 if user already exists
        return make_response(
            render_template('signup.html', error='Cette adresse mail est déjà utilisée pour un compte Aurore'), 202)


@app.route('/login', methods=['GET'])
def login_form():
    if request.args.get('next', ''):
        return render_template('login.html', error="Une authentification est nécessaire pour accéder à cette page")
    return render_template('login.html')


@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')


@app.route('/logout', methods=['POST'])
def logout():
    response = redirect(url_for('home_page'))
    response.delete_cookie('aurore_login')
    return response


@app.route('/administration', methods=['GET'])
@require_auth
def admin():
    offres = offres_service.get_all()
    unchecked = offres_service.get_unchecked()
    return make_response(render_template('offres.html', offres=offres, unchecked=unchecked), 200)


# route for logging user in
@app.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth:
        # returns 401 if any email or / and password is missing
        return make_response(render_template('login.html', error="Formulaire invalide"), 401)

    if not auth.get('email'):
        return make_response(
            render_template('login.html', error="Merci de renseigner le champ email"), 400)

    if not auth.get('password'):
        return make_response(
            render_template('login.html', error="Merci de renseigner le mot de passe"), 400)

    user = user_service.get_user_by_email(auth.get('email'))
    print(user)
    if not user:
        # returns 401 if user does not exist
        return make_response(render_template('login.html', error="Email invalide"), 400)

    if check_password_hash(user.pwd, str(auth.get('password'))):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=90)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        location = auth.get('next')

        if location:
            res = redirect(url_for(location))
        else:
            res = make_response(render_template('index.html'), 201)

        request.current_user = user
        res.set_cookie("aurore_login", token)

        return res
        # returns 403 if password is wrong
    return make_response(render_template('login.html', error="Mot de passe invalide"), 400)
