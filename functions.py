import requests
import pprint
import json
import pprint
import urllib.request


API_KEY = "d1d0ac42e23b49e887fce1fd9d410955"
Spoonacular_URL = "https://api.spoonacular.com/recipes/findByIngredients"

# Setting set ingredient
food = "apple, flour, milk"


def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request,

    return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode("utf-8")
        response_data = json.loads(response_text)
        # pprint.pprint(response_data)
    return response_data


# pprint.pprint(get_json(Spoonacular_URL))
def get_recipes_id_by_ingredient(ingredient):
    """
    Search recipe by ingredients
    Return a dictionary with recipe name as key and id as content
    """
    url = f"{Spoonacular_URL}?ingredients={ingredient}&apiKey={API_KEY}"

    # requests.get is another way to get information in a website
    # request function also provides status codes
    response = requests.get(url)

    dict = {}

    # Convert response into json format
    data = response.json()

    for recipes in data:
        name = recipes["title"]
        dict[name] = recipes["id"]
    return dict


pprint.pprint(get_recipes_id_by_ingredient(food))


def search_recipes_by_ingredient(ingredient):
    """
    Search recipes by inputing ingredient seperated by commas from Spoonacular API
    Returns a list of recipes names
    """
    data = get_recipes_id_by_ingredient(ingredient)

    list = []

    for names in data.keys():
        list.append(names)
    return list


# Test
recipes = search_recipes_by_ingredient(food)
pprint.pprint(recipes)


def get_recipet_id(recipe_name, ingredients):
    dict = get_recipes_id_by_ingredient(ingredients)

    for names in dict.keys():

        if names == recipe_name:
            return dict[names]


print(get_recipet_id("Easy Homemade Apple Fritters", food))


def get_recipe_info(recipe_name, ingredient):

    id = get_recipet_id(recipe_name, ingredient)

    url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey={API_KEY}"

    response = requests.get(url)

    data = response.json()
    return data


# pprint.pprint(get_recipe_info("Easy Homemade Apple Fritters", food))


def get_recipe_steps(recipe_name, ingredient):
    '''
    Inputs recipe name and available ingredient 
    Returns a dictionary with step number as key and instructions as items
    '''

    data = get_recipe_info(recipe_name, ingredient)

    steps = {}

    for instruction in data["analyzedInstructions"]:
        for step in instruction["steps"]:
            steps[f"Step {step["number"]}"] = step["step"]
    return steps


pprint.pprint(get_recipe_steps("Easy Homemade Apple Fritters", food))
