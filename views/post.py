import sqlite3
import json
from datetime import datetime


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


def create_post(post):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """ 
            INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved)
            VALUES (?, ?, ?, ?, ?, ?, 1)
            """,
            (
                post["user_id"],
                post["category_id"],
                post["title"],
                datetime.now(),
                post["image_url"],
                post["content"],
            ),
        )

        conn.commit()

        return db_cursor.lastrowid


def get_post(pk, query_params=None):
    if query_params and "_expand" in query_params:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                SELECT
                    p.id AS post_id,
                    p.title AS post_title,
                    p.content AS post_content,
                    p.publication_date AS publication_date,
                    u.id AS user_id,
                    u.username AS username
                FROM Posts p
                LEFT JOIN Users u ON u.id = user_id
                WHERE p.id = ?
                """,
                (pk,),
            )
            query_results = db_cursor.fetchone()

            if query_results:
                serialized_post = json.dumps(dict(query_results))
                return serialized_post
            else:
                return json.dumps({"error": "Post not found"})

    else:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                    SELECT
                        p.id,
                        p.title,
                        p.content,
                        p.publication_date,
                        u.username
                    FROM Posts p
                    LEFT JOIN Users u ON p.user_id = u.id
                    WHERE p.id = ?
                """,
                (pk,),
            )
            query_results = db_cursor.fetchone()

            if query_results:
                serialized_post = json.dumps(dict(query_results))
                return serialized_post
            else:
                return json.dumps({"error": "Post not found"})

            dictionary_version_of_object = dict(query_results)
            serialized_order = json.dumps(dictionary_version_of_object)

    return serialized_order
