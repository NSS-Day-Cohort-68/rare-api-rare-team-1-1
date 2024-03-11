import sqlite3
import json

def post_category(category_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO categories (label)
            VALUES (?)
            """,
            (category_data['label'],)
            )
        conn.commit()

    return True if db_cursor.rowcount > 0 else False


def get_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT label FROM categories 
            ORDER BY label ASC
            """
            )
        categories = [row[0] for row in db_cursor.fetchall()]
        serialized_categories = json.dumps(categories)
        return serialized_categories
    



