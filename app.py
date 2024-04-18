from flask import Flask, redirect, render_template, request, url_for
from functions import search_recipes_by_ingredient, get_recipe_steps


app = Flask(__name__, template_folder="templates")


@app.route("/")
def hello():
    return render_template("website.html")


@app.get("/recipe")
def get_recipe():
    return render_template("website.html")


@app.post("/recipe")
def find_recipe():
    ingredients = request.form["ingredients"]
    recipes = search_recipes_by_ingredient(ingredients)
    return render_template("render_page.html", result=recipes, input=ingredients)

@app.post("/recipe_info")
def recipe_info():
    choice = request.form.get("ChosenRecipe")  # Corrected from request.get

    ingredients = request.form["ingredients"]
    instructions = get_recipe_steps(choice, ingredients)
    return render_template("recipe_info.html", recipeName=choice, detail=instructions)


# This handles any 404 error for the website
@app.errorhandler(404)
def page_not_found(error):
    return (
        render_template(
            "error.html",
            error_message="There is an error.",
        ),
        404,
    )


if __name__ == "__main__":
    app.run(debug=True)
