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
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv
from spotifyapi import search, recommendedArtist

load_dotenv(find_dotenv())
app = flask.Flask(__name__)
app.secret_key = os.getenv("secretKey")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class users(db.Model, UserMixin):
    """creating user database"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)


class favSongs(db.Model):
    """creating favorite songs database"""

    id = db.Column(db.Integer, primary_key=True)
    song = db.Column(db.String(50))
    username = db.Column(db.String(50))


class favArtists(db.Model):
    """creating favorite artists database"""

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(50))
    username = db.Column(db.String(50))


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
    password = PasswordField(
        validators=[InputRequired(), Length(min=5, max=15)],
        render_kw={"placeholder": "Password"},
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
    password = PasswordField(
        validators=[InputRequired(), Length(min=5, max=15)],
        render_kw={"placeholder": "Password"},
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
            if bcrypt.check_password_hash(user.password, form.password.data):
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf8"
        )
        new_user = users(username=form.username.data, password=hashed_password)
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


# consider adding an edge case "where field is empty"
@app.route("/recommendations", methods=["GET", "POST"])
def recommendations():
    """recommendations page"""
    data = flask.request.form
    try:
        artist_id = search(data["song_title"])
        related_artists = recommendedArtist(artist_id)
        return flask.render_template(
            "recommendations.html", related_artists=related_artists
        )
    except:
        flask.flash("Please enter a song title")
        return flask.render_template("recommendations.html")


@app.route("/random", methods=["GET", "POST"])
def random():
    """random page"""
    return


@app.route("/favorites", methods=["GET", "POST"])
def favorites():
    """favorites page"""
    fav_songs = favSongs.query.filter_by(username=current_user.username).all()
    fav_artists = favArtists.query.filter_by(username=current_user.username).all()
    return flask.render_template(
        "favorites.html",
        num_songs=len(fav_songs),
        fav_songs=[favSong.song for favSong in fav_songs],
        num_artists=len(fav_artists),
        fav_artists=[favArtist.artist for favArtist in fav_artists],
    )


@app.route("/1", methods=["GET", "POST"])
def extra1():
    """extra route to work with"""
    return


@app.route("/2", methods=["GET", "POST"])
def extra2():
    """printing recommendations.html after searching api"""
    return flask.render_template("recommendations.html")


@app.route("/3", methods=["GET", "POST"])
def extra3():
    """extra"""
    return


@app.route("/4", methods=["GET", "POST"])
def extra4():
    """extra route to work with"""
    return


@app.route("/save_fav_song", methods=["GET", "POST"])
def save_fav_song():
    """allows user to save a song on the favorites page"""
    fav_song_name = flask.request.form.get("favSong")
    fav_song = favSongs(song=fav_song_name, username=current_user.username)
    db.session.add(fav_song)
    db.session.commit()
    return flask.redirect("/favorites")


@app.route("/del_fav_song", methods=["GET", "POST"])
def del_fav_song():
    """allows user to delete a song on the favorites page"""
    fav_song_name = flask.request.form.get("favSong")
    fav_song = favSongs.query.filter_by(
        song=fav_song_name, username=current_user.username
    ).first()
    if fav_song is not None:
        db.session.delete(fav_song)
        db.session.commit()
    return flask.redirect("/favorites")


@app.route("/save_fav_artist", methods=["GET", "POST"])
def save_fav_artist():
    """allows user to save a artist on the favorites page"""
    fav_artist_name = flask.request.form.get("favArtist")
    fav_artist = favArtists(artist=fav_artist_name, username=current_user.username)
    db.session.add(fav_artist)
    db.session.commit()
    return flask.redirect("/favorites")


@app.route("/del_fav_artist", methods=["GET", "POST"])
def del_fav_artist():
    """allows user to delete an artist on the favorites page"""
    fav_artist_name = flask.request.form.get("favArtist")
    fav_artist = favArtists.query.filter_by(
        artist=fav_artist_name, username=current_user.username
    ).first()
    if fav_artist is not None:
        db.session.delete(fav_artist)
        db.session.commit()
    return flask.redirect("/favorites")


app.run(debug=True)
