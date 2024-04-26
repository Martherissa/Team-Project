from flask import Flask, redirect, render_template, request, session, url_for
from functions import (
    search_recipes_by_ingredient,
    get_recipe_steps,
    get_recipe_image,
    get_recipe_summary,
    get_recipe_ingredients,
)

app = Flask(__name__, template_folder="templates")

# This is also learned from ChatGPT
# The key below is used to secure the session I mentioned below (similar to cookie or crypto in a sense)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        api_key = request.form["APIkey"]
        # I learned session from ChatGPT where it allows different webpages to access same information
        # In this case I stored username and apikey for easier reference in further reference
        session["username"] = username
        session["APIkey"] = api_key
        return redirect(url_for("hello"))
    return render_template("login.html")


@app.route("/welcome")
def hello():
    username = session.get("username")
    api_key = session.get("APIkey")
    return render_template("website.html", name=username, APIkey=api_key)


# # This chunck is no longer needed as we already stored the API key in session and there is not need to
# # defined any "get" action from here
# @app.get("/recipe")
# def get_recipe():
#     api_key = session.get("APIkey")
#     return render_template("website.html", APIkey=api_key)


@app.post("/recipe")
def find_recipe():
    api_key = session.get("APIkey")
    ingredients = request.form["ingredients"]
    recipes = search_recipes_by_ingredient(ingredients, api_key)
    return render_template("render_page.html", result=recipes, input=ingredients)


@app.post("/recipe_info")
def recipe_info():
    choice = request.form.get("ChosenRecipe")
    api_key = session.get("APIkey")
    ingredients = request.form["ingredients"]
    instructions = get_recipe_steps(choice, ingredients, api_key)
    all_ingredients = get_recipe_ingredients(choice, ingredients, api_key)
    images = get_recipe_image(choice, ingredients, api_key)
    summaries = get_recipe_summary(choice, ingredients, api_key)

    return render_template(
        "recipe_info.html",
        recipeName=choice,
        detail=instructions,
        summary=summaries,
        image=images,
        all_ingredient=all_ingredients,
    )


# This handles any 404 error for the website
@app.errorhandler(404)
def page_not_found(error):
    return (
        render_template(
            "error.html",
            error_message="There is an error",
        ),
        404,
    )


if __name__ == "__main__":
    app.run(debug=True)
