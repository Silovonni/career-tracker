import hashlib
import secrets
from database import get_connection


def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_password):
    try:
        salt, stored_hash = stored_password.split("$")

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        ).hex()

        return secrets.compare_digest(
            password_hash,
            stored_hash
        )

    except ValueError:
        return False


def create_user(name, email, password):
    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute(
            """
            INSERT INTO users
            (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (name, email, password_hash)
        )

        connection.commit()

        user_id = cursor.lastrowid

        return {
            "success": True,
            "user_id": user_id
        }

    except Exception as error:
        connection.rollback()

        return {
            "success": False,
            "error": str(error)
        }

    finally:
        connection.close()


def login_user(email, password):
    connection = get_connection()
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

    connection.close()

    if not user:
        return {
            "success": False,
            "error": "Invalid email or password."
        }

    if not verify_password(
        password,
        user["password_hash"]
    ):
        return {
            "success": False,
            "error": "Invalid email or password."
        }

    return {
        "success": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }