import psycopg2
import os
import json
from api_module import get_recipe_instructions
from dotenv import load_dotenv


load_dotenv() # load environment variables from the .env file


DATABASE_URL = os.getenv("DATABASE_URL")# retrieve the connection string from the environment variables


connection = psycopg2.connect(DATABASE_URL) # connect to the PostgreSQL database
cursor = connection.cursor()

def init_db():
    """Create the favorites table if it doesn't exist"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id SERIAL PRIMARY KEY,
            recipe_id INTEGER,
            title TEXT,
            instructions TEXT,
            used_ingredients TEXT,   
            missed_ingredients TEXT, 
            username TEXT DEFAULT 'default_user',
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    """Create the history_search table if it doesn't exist"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history_search (
            id SERIAL PRIMARY KEY,
            recipe_id INTEGER,
            title TEXT,
            instructions TEXT,
            used_ingredients TEXT,   
            missed_ingredients TEXT, 
            username TEXT DEFAULT 'default_user',
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()

def save_favorite(recipe, username='default_user'):
    """
    Save a favorite recipe to the database using f-string formatting
    username (str): The username to associate with the favorite default: 'default_user'
    """
    recipe_id = recipe.get('id')
    title = recipe.get('title')
    instructions = json.dumps(get_recipe_instructions(recipe.get('id')))
    used_ingredients = json.dumps(recipe.get('usedIngredients', []))
    missed_ingredients = json.dumps(recipe.get('missedIngredients', []))
    
    # build the SQL query using f-string (formatting denoted by f'''), used in this case for a multi-line string
    # the %s placeholders are for parameter substitution during query execution, ensuring safe insertion of values and preventing SQL injection
    query = f"""
        INSERT INTO favorites (recipe_id, title, instructions, used_ingredients, missed_ingredients, username)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    query_values = (
        recipe_id,
        title,
        instructions,
        used_ingredients,
        missed_ingredients,
        username
    )
    cursor.execute(query, query_values)
    connection.commit()

def get_favorites(username='default_user'):
    """
    Retrieve: favorite recipes for the given username.
    Returns:list of tuples: Each tuple contains (recipe_id, title, instructions, used_ingredients, missed_ingredients, date_added)
    """
    query = f"""
        SELECT recipe_id, title, instructions, used_ingredients, missed_ingredients, date_added 
        FROM favorites 
        WHERE username = %s
    """
    cursor.execute(query, (username,))
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def save_history_search(recipe, username='default_user'):
    """
    Save selected recipe history search to the database using f-string formatting
    username (str): The username to associate with the favorite default: 'default_user'
    """
    recipe_id = recipe.get('id')
    title = recipe.get('title')
    instructions = json.dumps(get_recipe_instructions(recipe.get('id')))
    used_ingredients = json.dumps(recipe.get('usedIngredients', []))
    missed_ingredients = json.dumps(recipe.get('missedIngredients', []))
    
    # build the SQL query using f-string (formatting denoted by f'''), used in this case for a multi-line string
    # the %s placeholders are for parameter substitution during query execution, ensuring safe insertion of values and preventing SQL injection
    query = f"""
        INSERT INTO history_search (recipe_id, title, instructions, used_ingredients, missed_ingredients, username)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    query_values = (
        recipe_id,
        title,
        instructions,
        used_ingredients,
        missed_ingredients,
        username
    )
    cursor.execute(query, query_values)
    connection.commit()

def get_history_search(username='default_user'):
    """
    retrieve history_search recipes for the given username.
    Returns a dictionary 
    """
    query = f"""
        SELECT recipe_id, title, instructions, used_ingredients, missed_ingredients, date_added 
        FROM history_search 
        WHERE username = %s
    """
    cursor.execute(query, (username,))
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


 
# print(f'''
#                 Recipe ID: {favorite.get(RECIPE_ID)},
#                 Title: {favorite.get(TITLE)},
#                 Used ingredient quantities: {used_ingredients},
#                 Unused ingredient quantities:{unused_ingredients}
#                 Instructions: {instructions}''')