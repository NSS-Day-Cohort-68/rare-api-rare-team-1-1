import sqlite3
import json


def post_category(category_data):
    with sqlite3.connect("./rare-api-rare-team-1-1/db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO categories (label)
            VALUES (?)
            """,
            (category_data['label'],)
            )

    return True if db_cursor.rowcount > 0 else False