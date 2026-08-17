from database import create_connection


def create_goals_table():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS career_goals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            title TEXT NOT NULL,

            description TEXT,

            status TEXT DEFAULT 'active',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)

        )
        """
    )

    connection.commit()
    connection.close()


def create_goal(
    user_id,
    title,
    description=""
):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO career_goals
        (
            user_id,
            title,
            description
        )

        VALUES (?, ?, ?)
        """,
        (
            user_id,
            title,
            description
        )
    )

    connection.commit()

    goal_id = cursor.lastrowid

    connection.close()

    return goal_id


def get_user_goals(user_id):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            description,
            status,
            created_at

        FROM career_goals

        WHERE user_id = ?

        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    goals = cursor.fetchall()

    connection.close()

    return goals


def complete_goal(
    user_id,
    goal_id
):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE career_goals

        SET status = 'completed'

        WHERE id = ?

        AND user_id = ?
        """,
        (
            goal_id,
            user_id
        )
    )

    connection.commit()
    connection.close()


def delete_goal(
    user_id,
    goal_id
):

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM career_goals

        WHERE id = ?

        AND user_id = ?
        """,
        (
            goal_id,
            user_id
        )
    )

    connection.commit()
    connection.close()