from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.post import Post

@app.route('/add/post', methods = ['POST'])
def add_post():
    if Post.validate_post(request.form):
        Post.post_save(request.form)
        print(request.form)
        return redirect('/dashboard')
    print("FAIL")
    return redirect('/add')

@app.route("/edit/<posts_id>", methods=['POST'])
def update(posts_id):
    if not Post.validate_post(request.form):
        flash("not successful")
        return redirect("/dashboard")
    Post.update_post(request.form, posts_id)
    return redirect("/dashboard")

@app.route("/delete/<posts_id>")
def delete(posts_id):
    Post.delete_post(posts_id)
    return redirect("/dashboard")
