import os
import uuid
from datetime import timedelta, datetime
from functools import wraps

import jwt
from flask import request, render_template, jsonify, make_response, redirect, url_for

from werkzeug.security import generate_password_hash, check_password_hash

from AuroreApp import app
from AuroreApp.user_service import MockUserService, User

user_service = MockUserService()

# TODO : Env
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
            return make_response(render_template('unauthorized.html'), 403)
        return f(*args, **kwargs)

    return decorated


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html", user=request.current_user)


@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html", user=request.current_user)


@app.route("/pro", methods=["GET"])
def pro():
    return render_template("faq.html", user=request.current_user)


@app.route("/particulier", methods=["GET"])
def particulier():
    return render_template("faq.html", user=request.current_user)


@app.route("/account", methods=["GET"])
@require_auth
def account():
    return make_response(render_template('account.html', user=request.current_user), 401)


# signup route
@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    email, identity = data.get('email'), data.get('identity')
    password = data.get('password')

    if not data:
        print("data")
        # returns 401 if any email or / and password is missing
        return make_response(render_template('signup.html', error="Formulaire invalide", user=request.current_user),
                             401)

    if not data.get('email'):
        print("email")
        return make_response(
            render_template('signup.html', error="Merci de renseigner le champ email", user=request.current_user), 400)

    if not data.get('password'):
        print("password")
        return make_response(
            render_template('signup.html', error="Merci de renseigner le mort de passe", user=request.current_user),
            400)

    # checking for existing user
    user = user_service.get_user_by_email(email)

    if not user:
        new_user = User(str(uuid.uuid4()), identity, email, generate_password_hash(password), False)
        user_service.add_user(new_user)
        return make_response(render_template('login.html', user=request.current_user), 201)
    else:
        # returns 202 if user already exists
        return make_response(
            render_template('signup.html', error='Cette adresse mail est déjà utilisée pour un compte Aurore',
                            user=request.current_user), 202)


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html', user=request.current_user)


@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html', user=request.current_user)


@app.route('/logout', methods=['POST'])
def logout():
    response = redirect(url_for('home_page'))
    response.delete_cookie('aurore_login')
    return response


# route for logging user in
@app.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth:
        print("auth")
        # returns 401 if any email or / and password is missing
        return make_response(render_template('login.html', error="Formulaire invalide", user=request.current_user), 401)

    if not auth.get('email'):
        print("email")
        return make_response(
            render_template('login.html', error="Merci de renseigner le champ email", user=request.current_user), 400)

    if not auth.get('password'):
        print("password")
        return make_response(
            render_template('login.html', error="Merci de renseigner le mot de passe", user=request.current_user), 400)

    user = user_service.get_user_by_email(auth.get('email'))
    if not user:
        # returns 401 if user does not exist
        return make_response(render_template('login.html', error="Email invalide", user=request.current_user), 400)

    if check_password_hash(user.pwd, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=90)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        res = make_response(render_template('index.html', user=user), 201)

        res.set_cookie("aurore_login", token)

        return res
        # returns 403 if password is wrong
    return make_response(render_template('login.html', error="Mot de passe invalide", user=request.current_user), 400)
