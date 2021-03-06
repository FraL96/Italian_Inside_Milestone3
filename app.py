import os
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRETKEY")

mongo = PyMongo(app)


@app.route("/")
# ------------------INDEX-------------------
@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")


# ------------------ALL RECIPES-------------------
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())

    return render_template("all_recipes.html", recipes=recipes)


# ------------------SEARCH-------------------
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("all_recipes.html",
                           recipes=recipes)


# ------------------RECIPE VIEW-------------------
@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    recipes = list(mongo.db.recipes.find({"_id": ObjectId(recipe_id)}))
    return render_template("recipe_view.html",
                           recipes=recipes)


# ------------------CASALE DEL GIGLIO-------------------
@app.route("/wine")
def wine():
    return render_template("wine.html")


# ------------------PROFILE-------------------
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if not session.get("user"):
        return render_template("error-handler/404-error.html")

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        if session["user"] == "admin":
            user_recipes = list(mongo.db.recipes.find())
        else:
            user_recipes = list(
                mongo.db.recipes.find({"created_by": session["user"]}))
        return render_template(
            "profile.html", username=username, user_recipes=user_recipes)
    return redirect(url_for("login"))


# ------------------ADDED BY ME-------------------
@app.route("/added_by_me/<username>")
def added_by_me(username):

    if not session.get("user"):
        return render_template("error-handler/404-error.html")

    recipes = list(mongo.db.recipes.find({"created_by": session["user"]}))
    return render_template("profile.html", username=session["user"],
                           recipes=recipes)


# ------------------ADD RECIPE-------------------
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():

    if not session.get("user"):
        return render_template("error-handler/404-error.html")

    if request.method == "POST":
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "region": request.form.get("region"),
            "category": request.form.get("category"),
            "option": request.form.get("option"),
            "difficulty": request.form.get("difficulty"),
            "quantity": request.form.get("quantity"),
            "ingredients": request.form.get("ingredients"),
            "wine_pairing": request.form.get("wine_pairing"),
            "preparation": request.form.get("preparation"),
            "picture": request.form.get("picture"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe added!")
        return redirect(url_for("profile", username=session["user"]))

    regions = mongo.db.regions.find().sort("region_name", 1)
    categories = mongo.db.categories.find().sort("category_name", 1)
    options = mongo.db.options.find().sort("option_name", 1)
    difficulty = mongo.db.difficulty.find().sort("difficulty_level", 1)
    return render_template("add_recipe.html", regions=regions,
                           categories=categories, options=options,
                           difficulty=difficulty)


# ------------------EDIT RECIPE-------------------
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):

    if not session.get("user"):
        return render_template("error-handler/404-error.html")

    elif request.method == "POST":
        info = {
            "recipe_name": request.form.get("recipe_name"),
            "region": request.form.get("region"),
            "category": request.form.get("category"),
            "option": request.form.get("option"),
            "difficulty": request.form.get("difficulty"),
            "quantity": request.form.get("quantity"),
            "ingredients": request.form.get("ingredients"),
            "wine_pairing": request.form.get("wine_pairing"),
            "preparation": request.form.get("preparation"),
            "picture": request.form.get("picture"),
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, info)
        flash("Recipe updated!")
        return redirect(url_for("profile", username=session["user"]))
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    regions = mongo.db.regions.find().sort("region_name", 1)
    categories = mongo.db.categories.find().sort("category_name", 1)
    options = mongo.db.options.find().sort("option_name", 1)
    difficulty = mongo.db.difficulty.find().sort("difficulty_level", 1)
    return render_template("edit_recipe.html", recipe=recipe, regions=regions,
                           categories=categories, options=options,
                           difficulty=difficulty)


# ------------------DELETE RECIPE-------------------
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):

    if not session.get("user"):
        return render_template("error-handler/404-error.html")

    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe deleted")
    return redirect(url_for("profile", username=session["user"]))


# ------------------LOGIN-------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("profile", username=session["user"]))

            else:
                flash("Ops! Username and/or Password are incorrect")
                return redirect(url_for("login"))

        else:
            flash("Ops! Username and/or Password are incorrect")
            return redirect(url_for("login"))

    return render_template("login.html")


# ------------------LOG OUT-------------------
@app.route("/logout")
def logout():
    flash("Come back soon!")
    session.pop("user")
    return redirect(url_for("login"))


# ------------------REGISTER-------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("This username already exists. Try again.")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


# ------------------MAIN-------------------
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
