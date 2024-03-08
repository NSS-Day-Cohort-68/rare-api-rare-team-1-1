import sqlite3
import json
from datetime import datetime


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            select id, username
            from Users
            where username = ?
            and password = ?
        """,
            (user["username"], user["password"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {"valid": True, "token": user_from_db["id"]}
        else:
            response = {"valid": False}

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Users (first_name, last_name, email, username, created_on, active) values (?, ?, ?, ?, ?, 1)
        """,
            (
                user["first_name"],
                user["last_name"],
                user["email"],
                user["username"],
                datetime.now(),
            ),
        )

        conn.commit()

        row_id = db_cursor.lastrowid

        return json.dumps({"token": row_id, "valid": True})


def find_email_match(email):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT id, email FROM Users WHERE email = ?
            """,
            (email,),
        )

        user_match = db_cursor.fetchone()

        if user_match is not None:
            response = {"email_exists": True}
        else:
            response = {"email_exists": False}

        return json.dumps(response)
