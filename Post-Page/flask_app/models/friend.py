from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Friend:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM friends;"
        results = connectToMySQL('post_page').query_db(query)
        all_friends = []
        for u in results:
            all_friends.append( cls(u) )
        return all_friends
    
    @classmethod
    def validate_friend(cls,data):
        is_valid = True
        if len(data["name"]) == 0:
            flash("Must pick a Name.")
            is_valid = False
        return is_valid 

    @classmethod
    def friend_add(cls, data):
        query = "INSERT into friends (name,user_id) values (%(name)s,%(user_id)s);"
        result = connectToMySQL('post_page').query_db(query, data)
        return result
    
    @classmethod
    def unadd(cls, friends_id):
        query = "DELETE from friends WHERE id = %(id)s;"
        data = {
            "id": friends_id
        }
        connectToMySQL('post_page').query_db(query,data)
        return friends_id