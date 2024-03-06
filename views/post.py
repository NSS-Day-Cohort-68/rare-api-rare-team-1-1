import sqlite3
import json


def get_all_user_posts(url):

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                p.id AS post_id,
                u.first_name AS author_name,
                p.title AS title_title,
                c.label AS categories_label,
                p.publication_date AS publication_date

                FROM Posts p
                LEFT JOIN Users u ON p.user_id = u.id
                LEFT JOIN Categories c ON p.category_id = c.id
                WHERE p.user_id = ?
                ORDER BY p.publication_date DESC
            """,
            (int(url["query_params"]["user_id"][0]),),
        )

        query_results = db_cursor.fetchall()

        posts = []

        for row in query_results:
            post = {
                "post_id": row["post_id"],
                "title": row["title_title"],
                "author": row["author_name"],
                "category": row["categories_label"],
            }
            posts.append(post)

        serialized_posts = json.dumps(posts)

    return serialized_posts
