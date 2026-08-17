import sqlite3
import os


# ============================================================
# CAREEROS DATABASE
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "careeros.db"
)


# ============================================================
# CONNECTION
# ============================================================

def create_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# Compatibility alias
def get_connection():

    return create_connection()


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():

    connection = create_connection()

    try:

        cursor = connection.cursor()


        # ====================================================
        # USERS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                email TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                career_goal TEXT DEFAULT '',

                education TEXT DEFAULT '',

                target_role TEXT DEFAULT '',

                experience_level TEXT DEFAULT '',

                study_hours INTEGER DEFAULT 0,

                projects_completed INTEGER DEFAULT 0,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP

            )
            """
        )


        # ====================================================
        # CAREER GOALS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS career_goals (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                title TEXT NOT NULL,

                description TEXT DEFAULT '',

                target_date TEXT,

                status TEXT DEFAULT 'active',

                progress INTEGER DEFAULT 0,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE

            )
            """
        )


        # ====================================================
        # PROJECTS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                description TEXT DEFAULT '',

                technology TEXT DEFAULT '',

                status TEXT DEFAULT 'planned',

                github_url TEXT DEFAULT '',

                live_url TEXT DEFAULT '',

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE

            )
            """
        )


        # ====================================================
        # JOB APPLICATIONS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                company TEXT NOT NULL,

                position TEXT NOT NULL,

                location TEXT DEFAULT '',

                application_date TEXT,

                status TEXT DEFAULT 'applied',

                salary TEXT DEFAULT '',

                job_url TEXT DEFAULT '',

                notes TEXT DEFAULT '',

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE

            )
            """
        )


        # ====================================================
        # SKILLS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS skills (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                category TEXT DEFAULT '',

                level INTEGER DEFAULT 1,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE

            )
            """
        )


        # ====================================================
        # STUDY SESSIONS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS study_sessions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                topic TEXT NOT NULL,

                hours REAL DEFAULT 0,

                notes TEXT DEFAULT '',

                session_date TEXT,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE

            )
            """
        )


        # ====================================================
        # ACTIVITY
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS activity (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                activity_type TEXT NOT NULL,

                description TEXT NOT NULL,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE

            )
            """
        )


        # ====================================================
        # AUTH SESSIONS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                session_token TEXT NOT NULL UNIQUE,

                expires_at TIMESTAMP,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE

            )
            """
        )


        # ====================================================
        # INDEXES
        # ====================================================

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_users_email
            ON users(email)
            """
        )


        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_goals_user
            ON career_goals(user_id)
            """
        )


        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_projects_user
            ON projects(user_id)
            """
        )


        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_applications_user
            ON applications(user_id)
            """
        )


        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_skills_user
            ON skills(user_id)
            """
        )


        connection.commit()

        print()
        print("========================================")
        print("        CAREEROS DATABASE")
        print("========================================")
        print("Database initialized successfully.")
        print()
        print(f"Database: {DATABASE_PATH}")
        print()
        print("Tables:")
        print("  ✓ users")
        print("  ✓ career_goals")
        print("  ✓ projects")
        print("  ✓ applications")
        print("  ✓ skills")
        print("  ✓ study_sessions")
        print("  ✓ activity")
        print("  ✓ sessions")
        print()
        print("CareerOS database initialized.")
        print()

    finally:

        connection.close()


# ============================================================
# STARTUP
# ============================================================

if __name__ == "__main__":

    initialize_database()