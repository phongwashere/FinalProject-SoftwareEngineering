"""
main app
"""
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
from random import choice
from spotifyapi import (
    search,
    recommendedartist,
    categoryplaylist,
    gettracks,
    getSongCover,
    getSongArtist,
    getSongName,
    getAlbum,
    getReleaseDate,
)

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
    pop = gettracks(categoryplaylist("pop"))
    hiphop = gettracks(categoryplaylist("hiphop"))
    rnb = gettracks(categoryplaylist("rnb"))
    country = gettracks(categoryplaylist("country"))
    return flask.render_template(
        "main.html", pop=pop, hiphop=hiphop, rnb=rnb, country=country
    )


@app.route("/landing", methods=["GET", "POST"])
@login_required
def landing():
    """landing page after using logs in"""
    user = current_user.username
    pop = gettracks(categoryplaylist("pop"))
    hiphop = gettracks(categoryplaylist("hiphop"))
    rnb = gettracks(categoryplaylist("rnb"))
    country = gettracks(categoryplaylist("country"))
    return flask.render_template(
        "landing.html", pop=pop, hiphop=hiphop, rnb=rnb, country=country, user=user
    )


@app.route("/recommendations", methods=["GET", "POST"])
@login_required
def recommendations():
    """recommendations page"""
    data = flask.request.form
    try:
        artist_id = search(data["song_title"])
        related_artists = recommendedartist(artist_id)
        return flask.render_template(
            "recommendations.html", related_artists=related_artists
        )
    except:
        flash = "Invalid, try again."
        return flask.render_template("recommendations.html", flash=flash)


@app.route("/random", methods=["GET", "POST"])
@login_required
def random():
    """random page"""
    return


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    """favorites page"""
    user = current_user.username
    fav_songs = favSongs.query.filter_by(username=current_user.username).all()
    fav_artists = favArtists.query.filter_by(username=current_user.username).all()
    return flask.render_template(
        "favorites.html",
        num_songs=len(fav_songs),
        fav_songs=[favSong.song for favSong in fav_songs],
        num_artists=len(fav_artists),
        fav_artists=[favArtist.artist for favArtist in fav_artists],
        user=user,
    )


@app.route("/1", methods=["GET", "POST"])
@login_required
def extra1():
    """no flash when loading page"""
    return flask.render_template("recommendations.html")


@app.route("/2/<song>", methods=["GET", "POST"])
@login_required
def extra2(song):
    """song information page route"""
    name = getSongName(song)
    artist = getSongArtist(song)
    album_cover = getSongCover(song)
    album_name = getAlbum(song)
    release_date = getReleaseDate(song)
    return flask.render_template(
        "songinfo.html",
        name=name,
        artist=artist,
        album_cover=album_cover,
        album_name=album_name,
        release_date=release_date,
    )


@app.route("/3", methods=["GET", "POST"])
@login_required
def extra3():
    """random song before clicking button"""
    return flask.render_template("randomb4song.html")


@app.route("/4", methods=["GET", "POST"])
@login_required
def extra4():
    """random song page"""
    genres = [
        "pop",
        "country",
        "rnb",
        "hiphop",
        "jazz",
        "latin",
        "rock",
        "classical",
    ]
    randomgenre = choice(genres)
    songs = gettracks(categoryplaylist(randomgenre))
    song = choice(songs)
    return flask.render_template("randompage.html", song=song)


@app.route("/save_fav_song", methods=["GET", "POST"])
@login_required
def save_fav_song():
    """allows user to save a song on the favorites page"""
    fav_song_name = flask.request.form.get("favSong")
    fav_song = favSongs(song=fav_song_name, username=current_user.username)
    db.session.add(fav_song)
    db.session.commit()
    return flask.redirect("/favorites")


@app.route("/del_fav_song", methods=["GET", "POST"])
@login_required
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
@login_required
def save_fav_artist():
    """allows user to save a artist on the favorites page"""
    fav_artist_name = flask.request.form.get("favArtist")
    fav_artist = favArtists(artist=fav_artist_name, username=current_user.username)
    db.session.add(fav_artist)
    db.session.commit()
    return flask.redirect("/favorites")


@app.route("/del_fav_artist", methods=["GET", "POST"])
@login_required
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


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
