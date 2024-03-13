import sqlite3
import json
from datetime import datetime


def get_all_user_posts(logged_in_user_id):

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
            (logged_in_user_id,),
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


def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT p.id, p.title, p.publication_date, p.user_id, u.first_name, u.last_name, u.email, u.username, p.category_id, c.label FROM Posts AS p
        LEFT JOIN Users AS u ON p.user_id = u.id
        LEFT JOIN Categories AS c ON p.category_id = c.id
        WHERE p.publication_date <= ?
        AND p.approved = 1
        ORDER BY p.publication_date DESC
            """,
            (datetime.today(),),
        )

        response = db_cursor.fetchall()

        posts = []
        for row in response:
            user = {
                "id": row["user_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "username": row["username"],
            }
            category = {"id": row["category_id"], "label": row["label"]}
            post = {
                "id": row["id"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "user": user,
                "category": category,
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


def get_post(pk):
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
                    p.image_url AS image_url,
                    p.user_id AS user_id,
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
