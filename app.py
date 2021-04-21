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
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    categories = list(mongo.db.categories.find())
    return render_template("all_recipes.html",
                           recipes=recipes, categories=categories)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("home_page.html", recipes=recipes)


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
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


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


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "region": request.form.get("region"),
            "category": request.form.get("category"),
            "option": request.form.get("option"),
            "difficulty": request.form.get("difficulty"),
            "quantity": request.form.get("quantity"),
            "ingredients": request.form.get("ingredients"),
            "step_1": request.form.get("step_1"),
            "step_2": request.form.get("step_2"),
            "step_3": request.form.get("step_3"),
            "step_4": request.form.get("step_4"),
            "step_5": request.form.get("step_5"),
            "step_6": request.form.get("step_6"),
            "step_7": request.form.get("step_7"),
            "step_8": request.form.get("step_8"),
            "step_9": request.form.get("step_9"),
            "step_10": request.form.get("step_10"),
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


@app.route("/view_recipe")
def view_recipe():
    return render_template("recipe_view.html")


@app.route("/homepage", methods=["GET"])
def homepage():
    return render_template("home_page.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
