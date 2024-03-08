import sqlite3
import json


def create_posttag(posttag):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """ 
            INSERT INTO PostTags (post_id, tag_id)
            VALUES (?, ?)
            """,
            (
                posttag["post_id"],
                posttag["tag_id"],
            ),
        )

        conn.commit()

        return db_cursor.lastrowid
