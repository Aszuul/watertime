from flask import Flask, render_template, request, url_for, redirect, flash
import requests
import os
import secrets
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from flask_bootstrap import Bootstrap5
from flask_caching import Cache

app = Flask("__main__")
app.config['SECRET_KEY'] = secrets.token_hex(16)
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap5(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
DB_URI = os.environ.get("SQLALCHEMY_DB_URI")

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    country_code: Mapped[int] = mapped_column(Integer)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)

def get_geodata(city, state, country_code):
    if state:
        res = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country_code}&limit=1&appid={WEATHER_API_KEY}").json()
    else:
        res = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country_code}&limit=1&appid={WEATHER_API_KEY}").json()
    lat = res[0]["lat"]
    lon = res[0]["lon"]
    return [lat, lon]

class Plant(db.Model):
    __tablename__ = "plants"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    symbol: Mapped[str] = mapped_column(String(100))


with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# @cache.cached(timeout=3600, key_prefix=current_user.name))
def get_weather():
    weather_url=f'https://api.openweathermap.org/data/2.5/weather?lat={current_user.lat}&lon={current_user.lon}&appid={WEATHER_API_KEY}'
    response = requests.get(weather_url)
    response.raise_for_status()
    data = response.json()
    weather = {
        "city": current_user.city,
        "state": current_user.state,
        "temp": int((data['main']['temp'] - 273) * 9/5 + 32),
        "description": data['weather'][0]['description'],
    }
    return weather


@app.route('/')
def home():
    # if logged in and location exists get weather data
    if current_user.is_authenticated:
        weather = get_weather()
    else:
        weather = ''
    return render_template('index.html', weather=weather)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user:
            flash("You've already signed up with that email, log in instead!", 'error')
            return redirect(url_for('login'))
        user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data,method="pbkdf2:sha256", salt_length=8),
            name=form.name.data.title(),
            city=form.city.data,
            state=form.state.data,
            country_code=form.country_code.data,
            lat = get_geodata(city=form.city.data, state=form.state.data, country_code=form.country_code.data)[0],
            lon = get_geodata(city=form.city.data, state=form.state.data, country_code=form.country_code.data)[1]
        )
        db.session.add(user)
        db.session.commit()
        login_user(user=user)
        return redirect(url_for('home'))
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in Successfully", 'success')
            return redirect(url_for('home'))
        else:
            flash("Invalid Email or Password", 'error')
            return redirect(url_for('login'))
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

