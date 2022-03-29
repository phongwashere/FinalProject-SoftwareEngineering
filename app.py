import os
import flask
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
app = flask.Flask(__name__)
app.secret_key = os.getenv("secretKey")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class users(db.Model, UserMixin):
    """creating user database"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """grabbing user_id to track"""
    return users.query.get(int(user_id))


class RegisterForm(FlaskForm):
    """creating a register form to sign up"""

    username = StringField(
        validators=[InputRequired(), Length(min=5, max=15)],
        render_kw={"placeholder": "Username"},
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        """raising validation errors"""
        existing_user_username = users.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "User already exists. Please choose a different username."
            )


class LoginForm(FlaskForm):
    """creating a login form to authentificate user"""

    username = StringField(
        validators=[InputRequired(), Length(min=5, max=15)],
        render_kw={"placeholder": "Username"},
    )
    submit = SubmitField("Login")


@app.route("/")
def firstpage():
    """sends to main"""
    return flask.redirect(flask.url_for("main"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """login application"""
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user)
            return flask.redirect(flask.url_for("landing"))
        else:
            flask.flash("User does not exist")
    return flask.render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """register account"""
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = users(username=form.username.data)
        db.session.add(new_user)
        db.session.commit()
        return flask.redirect(flask.url_for("login"))
    if users.query.filter_by(username=form.username.data).first():
        flask.flash("User already exists. Please choose a different username.")
    return flask.render_template("register.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """logging the user out"""
    logout_user()
    return flask.redirect(flask.url_for("login"))


@app.route("/main", methods=["GET", "POST"])
def main():
    """initial landing page"""
    return flask.render_template("main.html")


@app.route("/landing", methods=["GET", "POST"])
@login_required
def landing():
    """landing page after using logs in"""
    user = current_user.username
    return flask.render_template("landing.html", user=user)


@app.route("/recommendations", methods=["GET", "POST"])
def recommendations():
    """recommendations page"""
    return


@app.route("/random", methods=["GET", "POST"])
def random():
    """random page"""
    return


@app.route("/favorites", methods=["GET", "POST"])
def favorites():
    """favorites page"""
    return


@app.route("/1", methods=["GET", "POST"])
def extra1():
    """extra route to work with"""
    return


@app.route("/2", methods=["GET", "POST"])
def extra2():
    """extra route to work with"""
    return


@app.route("/3", methods=["GET", "POST"])
def extra3():
    """extra route to work with"""
    return


@app.route("/4", methods=["GET", "POST"])
def extra4():
    """extra route to work with"""
    return


app.run(debug=True)
