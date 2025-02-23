import psycopg2
import os
import json
from api_module import get_recipe_instructions
from dotenv import load_dotenv

load_dotenv()  # load environment variables from the .env file

DATABASE_URL = os.getenv("DATABASE_URL")  # retrieve the connection string

def init_db():
    """Create the favorites and history_search tables if they don't exist."""
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
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
    Save a favorite recipe to the database.
    The %s placeholders are for parameter substitution during query execution,
    ensuring safe insertion of values and preventing SQL injection.
    """
    recipe_id = recipe.get('id')
    title = recipe.get('title')
    instructions = json.dumps(get_recipe_instructions(recipe.get('id')))
    used_ingredients = json.dumps(recipe.get('usedIngredients', []))
    missed_ingredients = json.dumps(recipe.get('missedIngredients', []))
    
    query = """
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
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, query_values)
            connection.commit()

def get_favorites(username='default_user'):
    """
    Retrieve favorite recipes for the given username.
    Returns a list of dictionaries for each favorite recipe.
    """
    query = """
        SELECT recipe_id, title, instructions, used_ingredients, missed_ingredients, date_added 
        FROM favorites 
        WHERE username = %s
    """
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (username,))
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results

def save_history_search(recipe, username='default_user'):
    """
    Save a recipe search history to the database.
    The %s placeholders are for parameter substitution during query execution,
    ensuring safe insertion of values and preventing SQL injection.
    """
    recipe_id = recipe.get('id')
    title = recipe.get('title')
    instructions = json.dumps(get_recipe_instructions(recipe.get('id')))
    used_ingredients = json.dumps(recipe.get('usedIngredients', []))
    missed_ingredients = json.dumps(recipe.get('missedIngredients', []))
    
    query = """
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
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, query_values)
            connection.commit()

def get_history_search(username='default_user'):
    """
    Retrieve search history recipes for the given username.
    Returns a list of dictionaries for each history search record.
    """
    query = """
        SELECT recipe_id, title, instructions, used_ingredients, missed_ingredients, date_added 
        FROM history_search 
        WHERE username = %s
    """
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (username,))
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results
