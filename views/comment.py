import sqlite3
import json


def create_comment(comment_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """ 
            INSERT INTO Comments (author_id, post_id, content)
            VALUES (?, ?, ?)
            """,
            (
                comment_data["author_id"],
                comment_data["post_id"],
                comment_data["content"],
            ),
        )

        conn.commit()

        return db_cursor.lastrowid
