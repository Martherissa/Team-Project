import requests
import pprint
import json
import pprint
import urllib.request


MY_API_KEY = "d1d0ac42e23b49e887fce1fd9d410955"
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



def get_recipes_id_by_ingredient(ingredient, API_KEY):
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


def search_recipes_by_ingredient(ingredient, API_KEY):
    """
    Search recipes by inputing ingredient seperated by commas from Spoonacular API
    Returns a list of recipes names
    """
    data = get_recipes_id_by_ingredient(ingredient, API_KEY)

    list = []

    for names in data.keys():
        list.append(names)
    return list


def get_recipet_id(recipe_name, ingredients, API_KEY):
    '''
    Input recipe name, ingredients, and API key
    output the Spoonacular ID of the recipe
    '''
    dict = get_recipes_id_by_ingredient(ingredients, API_KEY)

    for names in dict.keys():

        if names == recipe_name:
            return dict[names]


def get_recipe_info(recipe_name, ingredient, API_KEY):
    '''
    Input recipe name, ingredients, and API key
    Output more information about the recipe based on Spoonacular Website
    '''

    id = get_recipet_id(recipe_name, ingredient, API_KEY)

    url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey={API_KEY}"

    response = requests.get(url)

    data = response.json()
    return data


def get_recipe_steps(recipe_name, ingredient, API_KEY):
    '''
    Inputs recipe name and available ingredient 
    Returns a dictionary with step number as key and instructions as items
    '''

    data = get_recipe_info(recipe_name, ingredient, API_KEY)

    steps = {}

    for instruction in data["analyzedInstructions"]:
        for step in instruction["steps"]:
            steps[f"Step {step["number"]}"] = step["step"]
    return steps


def get_recipe_ingredients(recipe_name, ingredient, API_KEY):
    '''
    Inputs recipe name and available ingredient 
    Returns a list of all ingredients needed and measurement in two forms
    '''

    data = get_recipe_info(recipe_name, ingredient, API_KEY)

    ingredients_dict = {}

    for instruction in data["extendedIngredients"]:

        ingredients = instruction['name']
        metric_amount = instruction['measures']['metric']['amount']
        metric_unit = instruction['measures']['metric']['unitShort']
        us_amount = instruction['measures']['us']['amount']
        us_unit = instruction['measures']['us']['unitShort']

        ingredients_dict[ingredients] = f"{metric_amount}{metric_unit} or {us_amount}{us_unit}"
        
    return ingredients_dict


def get_recipe_summary(recipe_name, ingredient, API_KEY):
    '''
    Inputs recipe name and available ingredient 
    Returns the summary of the recipe
    '''

    data = get_recipe_info(recipe_name, ingredient, API_KEY)

    summary = data["summary"]

    return summary



def get_recipe_image(recipe_name, ingredient, API_KEY):
    '''
    Inputs recipe name and available ingredient 
    Returns the image url of the recipe
    '''

    data = get_recipe_info(recipe_name, ingredient, API_KEY)

    picture = data["image"]

    return picture




def main():
    food = "apple, flour, milk"

    # recipes = search_recipes_by_ingredient(food, MY_API_KEY)
    # pprint.pprint(recipes)

    # pprint.pprint(get_recipe_info("Easy Homemade Apple Fritters", food, MY_API_KEY))

    # pprint.pprint(get_recipe_ingredients("Easy Homemade Apple Fritters", food, MY_API_KEY))

    # print(get_recipe_summary("Easy Homemade Apple Fritters", food, MY_API_KEY))

    # print(get_recipe_image("Easy Homemade Apple Fritters", food, MY_API_KEY))
    


if __name__ == "__main__":
    main()



