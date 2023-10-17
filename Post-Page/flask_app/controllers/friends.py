from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.friend import Friend

@app.route('/add/friend', methods = ['POST'])
def add_friend():
    if Friend.validate_friend(request.form):
        Friend.friend_add(request.form)
        print(request.form)
        return redirect('/friends')
    print("Unable to add")
    return redirect('/discover')

@app.route("/unadd/<friends_id>")
def unadd(friends_id):
    Friend.unadd(friends_id)
    return redirect("/friends")

