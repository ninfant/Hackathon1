import json
from api_module import get_recipe_instructions
from constants import INSTRUCTIONS, RECIPE_ID, TITLE, USED_INGREDIENTS

def display_main_menu():
    print("=== Recipe Book Menu ===")
    print("1. Search Recipes")
    print("2. Menu Suggestions")
    print("3. View Favorites")
    print("0. Exit")

def get_ingredients_input():
    ingredients = input("Enter available ingredients (separated by commas): ")
    # You can add validation here if needed
    return ingredients

def display_recipes(recipes):
    if not recipes:
        print("No recipes found.")
    for index, recipe in enumerate(recipes, start=1):
        print(f"{index}. {recipe.get('title')}")

def get_recipe_selection(recipes):
    try:
        choice = int(input("Select a recipe number to view details (0 to cancel): "))
        if choice == 0:
            return None
        return recipes[choice - 1] #if a user selects 1, subtracting 1 converts that selection to index 0, which is how python lists are indexed
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None

def display_recipe_details(recipe):
    print("\n=== Recipe Details ===")
    print("Title:", recipe.get('title'))
    print("ID:", recipe.get('id'))
    # Display used ingredients
    if 'usedIngredients' in recipe and recipe['usedIngredients']:
        print("\nThe Ingredients you provided:")
        for ingredient in recipe['usedIngredients']:
            name = ingredient.get('name')
            amount = ingredient.get('amount')
            unit = ingredient.get('unit')
            print(f" - {name}: {amount} {unit}")
    else:
        print("\nSeems like you don't have enough ingredients for the recipe, here below you have a suggestion of what you need")
    # Display missed ingredients
    if 'missedIngredients' in recipe and recipe['missedIngredients']:
        print("\nMissing ingredients you need to complete your recipe:")
        for ing in recipe['missedIngredients']:
            name = ing.get('name')
            amount = ing.get('amount')
            unit = ing.get('unit')
            print(f" - {name}: {amount} {unit}")
    else:
        print("\nMissed Ingredients: Not available")
    # Display instructions if available
    instructions = get_recipe_instructions(recipe.get('id'))
    if instructions is not None:
        print("\nRecipe Instructions:")
        for index, step in enumerate(instructions, 1):
            print(f"{index}. {step}")
    else:
        print("\n No more Instructions")

def ask_mark_favorite():
 while True:
    choice = input("Mark this recipe as favorite? (y/n): ").strip().lower() # strip() to removes whitespace and lower() converts the input to lowercase for the user input
    if choice in ('y', 'n'):
        if choice == 'y':
            return True
        else:
            return False
    else:
        print("Please enter 'y' or 'n'.")


def display_favorites(favorites):
    if not favorites:
        print("No favorites found.")
    else:
        print("=== Favorite Recipes ===")
        for favorite in favorites:
            used_ingredients=[]
            unused_ingredients=[]
            for ingredient in json.loads(favorite.get('used_ingredients', [])):
                used_ingredients.append(ingredient.get('original'))
            for ingredient in json.loads(favorite.get('missed_ingredients', [])):
                unused_ingredients.append(ingredient.get('original'))
            instructions = favorite.get(INSTRUCTIONS, '')
            print(f"""
Recipe ID: {favorite.get(RECIPE_ID, 'N/A')}
Title: {favorite.get(TITLE, 'No Title')}

Used Ingredient Quantities:   {used_ingredients}
Unused Ingredient Quantities: {unused_ingredients}

Instructions:
{instructions}
-----------------------------------------------------
""")
            

def display_menu(favorite_menu, saved_history_search):
    # to combine the two lists using concatenation, 
    # a list from the favorites and a list from the selected recipies history

    combined_menu = favorite_menu + saved_history_search
    print("=== Weekly Menu Suggestions ===")
    print("                               ")
    for item in combined_menu:
        print("--------------------------------")
        print(item)
    print("--------------------------------")
    print("                               ")   
   

