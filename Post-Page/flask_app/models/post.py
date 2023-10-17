from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Post:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id;"
        results = connectToMySQL('post_page').query_db(query)
        all_posts = []
        for row in results:
            one_post = cls(row)
            user_info = { 
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
          
            user = User(user_info)
            one_post.user = user
            all_posts.append(one_post)
        return all_posts
    
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM posts WHERE posts.id = %(id)s;"
        result = connectToMySQL('post_page').query_db(query,data)  
        return cls(result[0])
    
    @classmethod
    def validate_post(cls, data):
        is_valid = True
        if len(data["title"]) == 0:
            flash("Must have a title.")
            is_valid = False
        if len(data["content"]) == 0:
            flash("Must have content")
            is_valid = False
        return is_valid
    
    @classmethod
    def post_save(cls, data):
        if not cls.validate_post(data):
            print("not validated")
            return False
        query = "INSERT into posts (title,content,user_id) values (%(title)s,%(content)s,%(user_id)s);"
        result = connectToMySQL('post_page').query_db(query, data)
        return result
    
    @classmethod
    def update_post(cls, data, id):
        query = """UPDATE posts SET title = %(title)s,content = %(content)s
        WHERE id = {};""".format(id)
        results = connectToMySQL('post_page').query_db(query,data)
        return results
    
    @classmethod
    def delete_post(cls, posts_id):
        query = "DELETE from posts WHERE id = %(id)s;"
        data = {
            "id": posts_id
        }
        connectToMySQL('post_page').query_db(query,data)
        return posts_id
    
    