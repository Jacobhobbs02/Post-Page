from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.friend import Friend
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sources')
def sources():
    return render_template('sources.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/account')
    
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/account')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/account')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard/')
def dashboard():

    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    all_posts = Post.get_all()
    return render_template("dashboard.html",user = User.get_one(data), posts = all_posts)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/add')
def add():
    data = {
        'id': session['user_id']
    }
    return render_template("add.html", user=User.get_one(data))

@app.route('/edit/<posts_id>')
def edit(posts_id):
    data = {
        'id': posts_id
    }
    one_post = Post.get_one(data)
    return render_template("edit.html", posts = one_post)


@app.route('/discover')
def discover():
    data = {
        'id': session['user_id']
    }

    all_users = User.get_all()
    return render_template("discover.html", users = all_users,user=User.get_one(data))

@app.route('/friends')
def friends():
    data = {
        'id': session['user_id']
    }

    all_friends = Friend.get_all()

    return render_template("friends.html", friends = all_friends,user=User.get_one(data))

@app.route('/Myprofile')
def Myprofile():
    data = {
        'id': session['user_id']
    }
    all_posts = Post.get_all()
    return render_template("profile.html", user=User.get_one(data), posts = all_posts)

@app.route('/update/<users_id>',methods=['POST'])
def update_user(users_id):
    if not User.validate_user(request.form):
        return redirect("/edit")
    User.update_user(request.form, users_id)
    return redirect('/dashboard')

@app.route("/delete/account/<users_id>")
def delete_account(users_id):
    User.delete_account(users_id)
    return redirect("/")