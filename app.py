from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import LoginForm, SignUpForm, FeedbackForm

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
    if "username" not in session or username != session['username']:
        flash("Please login to see the secret")
        return redirect('/login')
    u = User.query.filter_by(username = username).first()
    return render_template('/user.html', user = u)

@app.route('/users/<username>/feedback', methods = ["GET", "POST"])
def feedback_form(username):
    if "username" not in session or username != session['username']:
        flash("Please login to see the secret")
        return redirect('/login')
    u = User.query.filter_by(username = username).first()
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(username = u.username, title = title, content = content)
        send_to_server(feedback)
        return redirect(f'/users/{u.username}')
    return render_template('/feedback.html', user = u, form = form)

@app.route('/users/<username>/delete')
def delete_user(username):
    if "username" not in session or username != session['username']:
        flash("Please Login")
        return redirect('/login')
    u = User.query.get(username)
    db.session.delete(u)
    db.session.commit()
    session.pop('username')
    return redirect('/')


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
        send_to_server(new_user)
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


def send_to_server(item):
    db.session.add(item)
    db.session.commit()
    return True