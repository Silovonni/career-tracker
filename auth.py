import hashlib
import secrets

from database import create_connection


# ============================================================
# PASSWORD SECURITY
# ============================================================

def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_password):
    try:
        salt, stored_hash = stored_password.split("$", 1)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000
        ).hex()

        return secrets.compare_digest(
            password_hash,
            stored_hash
        )

    except (ValueError, AttributeError):
        return False


# ============================================================
# AUTHENTICATION TABLE
# ============================================================

def create_auth_table():
    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id)
                    REFERENCES users(id)
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


# ============================================================
# CREATE USER
# ============================================================

def create_user(name, email, password):

    connection = create_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            return {
                "success": False,
                "error": "An account with that email already exists."
            }

        password_hash = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password_hash
            )
        )

        connection.commit()

        user_id = cursor.lastrowid

        return {
            "success": True,
            "user_id": user_id,
            "name": name,
            "email": email
        }

    except Exception as error:

        connection.rollback()

        return {
            "success": False,
            "error": str(error)
        }

    finally:

        connection.close()


# ============================================================
# AUTHENTICATE USER
# ============================================================

def authenticate_user(email, password):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

    finally:

        connection.close()

    if not user:

        return {
            "success": False,
            "error": "Invalid email or password."
        }

    try:

        user_id = user["id"]
        name = user["name"]
        user_email = user["email"]
        stored_password = user["password_hash"]

    except (TypeError, KeyError):

        user_id = user[0]
        name = user[1]
        user_email = user[2]
        stored_password = user[3]

    if not verify_password(
        password,
        stored_password
    ):

        return {
            "success": False,
            "error": "Invalid email or password."
        }

    return {
        "success": True,
        "user": {
            "id": user_id,
            "name": name,
            "email": user_email
        }
    }


# ============================================================
# LOGIN ALIAS
# ============================================================

def login_user(email, password):

    return authenticate_user(
        email,
        password
    )


# ============================================================
# EMAIL CHECK
# ============================================================

def email_exists(email):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        return user is not None

    finally:

        connection.close()


# ============================================================
# GET USER
# ============================================================

def get_user_by_id(user_id):

    connection = create_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                email
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            return None

        try:

            return {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }

        except (TypeError, KeyError):

            return {
                "id": user[0],
                "name": user[1],
                "email": user[2]
            }

    finally:

        connection.close()


# ============================================================
# INITIALIZE
# ============================================================

if __name__ == "__main__":

    create_auth_table()

    print("CareerOS authentication initialized.")