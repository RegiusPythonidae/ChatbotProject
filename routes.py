from flask import render_template, url_for, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
import requests
import json

from forms import RegisterForm, MessageForm, LoginForm
from extensions import app, db
from models import Message, User


RASA_LINK = "http://127.0.0.1:5005"
@app.route("/", methods=["GET", "POST"])
def home():
    form = MessageForm()
    if form.validate_on_submit():
        data = {
            "sender": current_user.username,
            "message": form.message.data
        }
        response = requests.post(f"{RASA_LINK}/webhooks/rest/webhook", data=json.dumps(data))
        if response.status_code == 200:
            user_message = Message(text=form.message.data, sent_time=datetime.now(), user_id=current_user.id, is_chatbot=False)
            user_message.create()

            bot_response = response.json()[0]["text"]
            bot_message = Message(text=bot_response, sent_time=datetime.now(), user_id=current_user.id, is_chatbot=True)
            bot_message.create()

        return redirect(url_for("home"))

    return render_template("index.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    birthday=form.birthday.data,
                    country=form.country.data,
                    gender=form.gender.data)
        user.create()
        return redirect(url_for("login"))

    print(form.errors)
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # form.username.data
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get("next")
            if next:
                return redirect(next)
            return redirect(url_for("home"))

    print(form.errors)
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")
