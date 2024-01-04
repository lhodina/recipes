from flask import render_template, redirect, request, session

from flask_app import app
from flask_app.models import recipe


@app.route("/recipes")
def get_recipes():
    if session and session["current_user"]:
        all_recipes = recipe.Recipe.get_all()
        return render_template("recipes.html", all_recipes=all_recipes)
    else:
        return render_template("unauthorized.html")


@app.route("/recipes/create")
def get_new_recipe_form():
    return render_template("new_recipe_form.html")


@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    data = {
        "user_id": request.form["user_id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_thirty": request.form["under_thirty"],
        "date_made": request.form["date_made"]
    }

    session["data"] = data
    if not recipe.Recipe.validate_recipe(data):
        return redirect("/recipes/create")
    session.pop("data")
    recipe.Recipe.save(data)
    return redirect("/recipes")


@app.route("/recipes/<int:recipe_id>")
def get_recipe(recipe_id):
    data = {"id": recipe_id}
    current_recipe = recipe.Recipe.get_one(data)
    return render_template("recipe.html", recipe=current_recipe)


@app.route("/recipes/edit/<int:recipe_id>")
def get_edit_recipe_form(recipe_id):
    data = {"id": recipe_id}
    current_recipe = recipe.Recipe.get_one(data)
    return render_template("edit_recipe_form.html", recipe=current_recipe)


@app.route("/edit_recipe", methods=["POST"])
def update_recipe():
    data = {
        "id": request.form["id"],
        "user_id": request.form["user_id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_thirty": request.form["under_thirty"],
        "date_made": request.form["date_made"]
    }

    if not recipe.Recipe.validate_recipe(data):
        return redirect(f"/recipes/edit/{data['id']}")
    recipe.Recipe.update(data)
    return redirect("/recipes")


@app.route("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    data = {"id": recipe_id}
    recipe.Recipe.delete(data)
    return redirect("/recipes")
