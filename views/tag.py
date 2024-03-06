import sqlite3
import json


def create_tag(tag_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """ 
            INSERT INTO Tags (label)
            VALUES (?)
            """,
            (tag_data["label"],),
        )

        conn.commit()

        return db_cursor.lastrowid
