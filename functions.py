import requests

API_KEY = "d1d0ac42e23b49e887fce1fd9d410955"
Spoonacular_URL = "https://api.spoonacular.com/recipes/findByIngredients"


def search_recipes_by_ingredient(ingredient):
    url = f"{Spoonacular_URL}?ingredients={ingredient}&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None


ingredient = input("Enter an ingredient to search recipes: ")
recipes = search_recipes_by_ingredient(ingredient)

if recipes:
    print("Recipes found:")
    for recipe in recipes:
        print(recipe["title"])
else:
    print("No recipes found.")
