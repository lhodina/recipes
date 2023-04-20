from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app import app
from flask_app.models import user

class Recipe():
    DB = "recipes"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.under_thirty = data["under_thirty"]
        self.date_made = data["date_made"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM recipes
        LEFT JOIN users ON recipes.user_id = users.id
        """
        results = connectToMySQL(cls.DB).query_db(query)
        all_recipes= []
        for row in results:
            current_recipe = cls(row)
            current_recipe_user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            author = user.User(current_recipe_user_data)
            current_recipe.creator = author
            all_recipes.append(current_recipe)
        return all_recipes

    @classmethod
    def get_one(cls, data):
        query = """
        SELECT * FROM recipes
        LEFT JOIN users ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)[0]
        current_recipe = cls({
            "id": result["id"],
            "name": result["name"],
            "description": result["description"],
            "instructions": result["instructions"],
            "date_made": result["date_made"],
            "under_thirty": result["under_thirty"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"]
            })
        current_recipe_user_data = {
            "id": result["users.id"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "email": result["email"],
            "password": result["password"],
            "created_at": result["users.created_at"],
            "updated_at": result["users.updated_at"]
        }
        author = user.User(current_recipe_user_data)
        current_recipe.creator = author
        return current_recipe


    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO recipes(name, description, instructions, under_thirty, date_made, user_id)
        VALUES ( %(name)s, %(description)s, %(instructions)s, %(under_thirty)s, %(date_made)s, %(user_id)s );
        """
        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def update(cls, data):
        query = """
        UPDATE recipes
        SET
        name=%(name)s,
        description=%(description)s,
        instructions=%(instructions)s,
        under_thirty=%(under_thirty)s,
        date_made=%(date_made)s,
        user_id=%(user_id)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if not recipe["name"]:
            flash("Name required")
            is_valid = False
        if len(recipe["name"]) < 3:
            flash("Name must be at least three characters")
            is_valid = False
        if not recipe["description"]:
            flash("Description required")
            is_valid = False
        if len(recipe["description"]) < 3:
            flash("Description must be at least three characters")
            is_valid = False
        if not recipe["instructions"]:
            flash("Instructions required")
            is_valid = False
        if len(recipe["instructions"]) < 3:
            flash("Instructions must be at least three characters")
            is_valid = False
        if not recipe["date_made"]:
            flash("Date cooked/made required")
            is_valid = False
        # under_thirty already checked by default
        return is_valid
