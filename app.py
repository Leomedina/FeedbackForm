from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import LoginForm, SignUpForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "SECRET"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_home():
    return redirect('/register')

@app.route('/users/<username>')
def show_userpage(username):
    if "username" not in session:
        flash("Please login to see the secret")
        return redirect('/login')
    u = User.query.filter_by(username = username).first()
    return render_template('/user.html', user = u)

@app.route('/register', methods = ["GET", "POST"])
def register_user():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        flash('Success! Created new account')
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(f'/users/{username}')
    return render_template('/signup.html', form = form)

@app.route('/login', methods = ["GET", "POST"])
def authenticate_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if User.authenticate(username, password):
            flash('LOGIN Successful')
            session['username'] = username
            return redirect(f'/users/{username}')
        else: 
            form.username.errors = ["Invalid Username/Password"]
    return render_template('/login.html', form = form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!")
    return redirect('/')