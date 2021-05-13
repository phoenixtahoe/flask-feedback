from flask import Flask, request, redirect, render_template, jsonify, session
from models import db, connect_db, User, Feedback
from forms import registerForm, loginForm, feedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

connect_db(app)
db.create_all()

@app.route("/")
def root():
    return redirect('/register')

@app.route("/register")
def renderRegister():

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = registerForm()
    return render_template("user/new.html", form=form)

@app.route("/register", methods=["POST"])
def createUser():
    form = registerForm()
    user = User.register(
    form.username.data, 
    form.password.data, 
    form.email.data, 
    form.first_name.data, 
    form.last_name.data
    )

    session['username'] = user.username
    db.session.commit()

    return redirect(f"/users/{user.username}")

@app.route('/login')
def renderLogin():
    form = loginForm()
    return render_template("user/login.html", form=form)

@app.route('/login', methods=["POST"])
def loginUser():
    form = loginForm()
    user = User.auth(form.username.data, form.password.data)
    if user:
        session['username'] = user.username
        return redirect(f"/users/{user.username}")
    else:
        return render_template("user/login.html", form=form)

@app.route("/users/<username>")
def showUser(username):

    if "username" not in session or username != session['username']:
        return redirect('/login')

    user = User.query.get(username)

    return render_template("user/show.html", user=user)

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>/delete")
def deleteUser(username):

    if "username" not in session or username != session['username']:
        return redirect('/')

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>/feedback/new")
def renderFeedback(username):

    if "username" not in session or username != session['username']:
        return redirect('/')

    form = feedbackForm()
        
    return render_template("feedback/new.html", form=form)

@app.route("/users/<username>/feedback/new", methods=["POST"])
def createFeedback(username):

    if "username" not in session or username != session['username']:
        return redirect('/')

    form = feedbackForm()

    feedback = Feedback(title=form.title.data, content=form.content.data, username=username,)

    db.session.add(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")

@app.route("/feedback/<int:feedback_id>/update")
def editForm(feedback_id):
    
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return redirect('/')

    form = feedbackForm(obj=feedback)

    return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/update", methods=["POST"])
def updateFeedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return redirect('/')

    form = feedbackForm()

    feedback.title = form.title.data
    feedback.content = form.content.data

    db.session.commit()

    return redirect(f"/users/{feedback.username}")

@app.route("/feedback/<int:feedback_id>/delete")
def delete_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return redirect('/')

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")