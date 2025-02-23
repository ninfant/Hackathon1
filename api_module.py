import requests
import json

def search_recipes(ingredients):
  
    api_key = '18e0c86a23314a89a69e4a95443b3582'   #Spoonacular API key
    base_url = 'https://api.spoonacular.com/recipes/findByIngredients'

    # Set up the parameters for the request
    params = {
        'ingredients': ingredients,  # Ingredients entered by the user (e.g., "tomato,cheese")
        'number': 5,                 # Maximum number of recipes to return
        'ranking': 1,                # 1: maximize used ingredients; 2: minimize missing ingredients
        'ignorePantry': 'true',      # Ignore common pantry items
        'apiKey': api_key
    }
   
    response = requests.get(base_url, params=params) # this make the GET request to the API
    
    if response.status_code == 200: # if the response is successful
        return response.json() #  will be converted into a python object (list or dictionaries)
    else:
        print("API Error:", response.status_code)
        print("Response:", response.text)
        return None

 

def get_recipe_instructions(recipe_id):
    """
    Retrieves the step-by-step instructions for a given recipe ID
    from the Spoonacular API and returns a list of step descriptions.
    """
    api_key = '18e0c86a23314a89a69e4a95443b3582'
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions"
    params = {
        'apiKey': api_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        instructions_data = response.json() # The API returns a list with the instructions, they should always come in the first position
        if instructions_data and len(instructions_data) > 0:
            steps = instructions_data[0].get('steps', [])
            step_descriptions = []
            for step in steps:
                description = step.get('step')
                step_descriptions.append(description)
            return step_descriptions  # return all the steps in the instructions list
        else:
            print("No instructions found for this recipe.")
            return []
    else:
        print("Error:", response.status_code)
        print("Response:", response.text)
        return None
