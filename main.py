import api_module
from constants import TITLE
import db_module
import ui_module
import re

def favorite_menu(favorites):
    menu = []
    for fav in favorites:
     menu.append(fav[TITLE])
    return menu #return a list of titles from favorites

def saved_history_search(selected_recipe_history):
    menu= []
    for selected in selected_recipe_history:
        menu.append(selected.get('title'))
    return menu

def main():
    db_module.init_db()    # Initialize the database (create tables if not exist)

    while True:
        ui_module.display_main_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            ingredients = ui_module.get_ingredients_input()
            if not ingredients:
                print ('The input cannot be empty: ')
                break
            elif re.search(r"\d", ingredients):
                print("The input must not contain numbers.")
                break
            else:
             recipes = api_module.search_recipes(ingredients)
             if recipes:
                ui_module.display_recipes(recipes)
             else:
                 print('Please enter real ingredients')
                 break                                  
             selected_recipe = ui_module.get_recipe_selection(recipes)
            if selected_recipe:
                ui_module.display_recipe_details(selected_recipe)
                if ui_module.ask_mark_favorite(): #If this is True, goes in next step 
                    db_module.save_favorite(selected_recipe)
                else:
                    db_module.save_history_search(selected_recipe)
        elif choice == "2":
            favorites = db_module.get_favorites()
            fav_menu = favorite_menu(favorites)
            selected_recipe_history = db_module.get_history_search()
            history_search = saved_history_search(selected_recipe_history)
            ui_module.display_menu(fav_menu, history_search)
        elif choice == "3":
            favorites = db_module.get_favorites()
            ui_module.display_favorites(favorites)
        elif choice == "0":
            print("Exiting the application....")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
