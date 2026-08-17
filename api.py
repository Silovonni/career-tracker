from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from itsdangerous import URLSafeSerializer

from database import create_connection
from auth import create_user, login_user
from goals import (
    create_goals_table,
    create_goal,
    get_user_goals,
    complete_goal,
    delete_goal
)


app = FastAPI(
    title="CareerOS API",
    version="1.0.0"
)


# ============================================================
# DATABASE
# ============================================================

create_goals_table()


# ============================================================
# SESSION
# ============================================================

SECRET_KEY = "careeros-development-secret-change-before-production"

serializer = URLSafeSerializer(
    SECRET_KEY,
    salt="careeros-session"
)


COOKIE_NAME = "careeros_session"


def set_session(response, user_id):

    token = serializer.dumps({
        "user_id": user_id
    })

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 60 * 24 * 7
    )


def get_current_user_id(request):

    token = request.cookies.get(
        COOKIE_NAME
    )

    if not token:
        return None

    try:

        data = serializer.loads(
            token
        )

        return int(
            data["user_id"]
        )

    except Exception:

        return None


def require_user(request):

    user_id = get_current_user_id(
        request
    )

    if user_id is None:

        raise HTTPException(
            status_code=401,
            detail="Not logged in."
        )

    return user_id


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


# ============================================================
# FRONTEND
# ============================================================

@app.get("/")
def home():

    return FileResponse(
        "frontend/index.html"
    )


@app.get("/auth")
def auth_page():

    return FileResponse(
        "frontend/auth.html"
    )


@app.get("/dashboard")
def dashboard_page():

    return FileResponse(
        "frontend/dashboard.html"
    )


@app.get("/goals")
def goals_page():

    return FileResponse(
        "frontend/goals.html"
    )


# ============================================================
# REQUEST MODELS
# ============================================================

class RegisterRequest(BaseModel):

    name: str
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):

    email: EmailStr
    password: str


class GoalRequest(BaseModel):

    title: str
    description: str = ""


# ============================================================
# REGISTER
# ============================================================

@app.post("/api/auth/register")
def register(request: RegisterRequest):

    result = create_user(
        request.name,
        request.email,
        request.password
    )

    if not result["success"]:

        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return {
        "success": True,
        "user_id": result["user_id"],
        "message": "Account created successfully."
    }


# ============================================================
# LOGIN
# ============================================================

@app.post("/api/auth/login")
def login(
    request: LoginRequest,
    response: Response
):

    result = login_user(
        request.email,
        request.password
    )

    if not result["success"]:

        raise HTTPException(
            status_code=401,
            detail=result["error"]
        )


    user_id = result["user"]["id"]


    set_session(
        response,
        user_id
    )


    return {
        "success": True,
        "user": result["user"]
    }


# ============================================================
# CURRENT USER
# ============================================================

@app.get("/api/auth/me")
def get_current_user(
    request: Request
):

    user_id = require_user(
        request
    )


    connection = create_connection()

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

    connection.close()


    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )


    goals = get_user_goals(
        user_id
    )


    active_goals = sum(
        1
        for goal in goals
        if goal["status"] == "active"
    )


    return {
        "success": True,

        "user": {

            "id": user["id"],

            "name": user["name"],

            "email": user["email"],

            "target_role": None,

            "career_goal": None,

            "education": None,

            "experience_level": None,

            "career_progress": 0,

            "active_goals": active_goals,

            "projects_count": 0,

            "applications_count": 0,

            "goals": goals

        }
    }


# ============================================================
# LOGOUT
# ============================================================

@app.post("/api/auth/logout")
def logout(
    response: Response
):

    response.delete_cookie(
        COOKIE_NAME
    )

    return {
        "success": True,
        "message": "Logged out successfully."
    }


# ============================================================
# GOALS
# ============================================================

@app.get("/api/goals")
def list_goals(
    request: Request
):

    user_id = require_user(
        request
    )


    goals = get_user_goals(
        user_id
    )


    return [

        {
            "id": goal["id"],
            "title": goal["title"],
            "description": goal["description"],
            "status": goal["status"],
            "created_at": goal["created_at"]
        }

        for goal in goals

    ]


# ============================================================
# CREATE GOAL
# ============================================================

@app.post("/api/goals")
def add_goal(
    request: Request,
    goal: GoalRequest
):

    user_id = require_user(
        request
    )


    title = goal.title.strip()

    description = goal.description.strip()


    if not title:

        raise HTTPException(
            status_code=400,
            detail="Goal title is required."
        )


    goal_id = create_goal(
        user_id,
        title,
        description
    )


    return {
        "success": True,
        "goal_id": goal_id,
        "message": "Goal created successfully."
    }


# ============================================================
# COMPLETE GOAL
# ============================================================

@app.post("/api/goals/{goal_id}/complete")
def finish_goal(
    request: Request,
    goal_id: int
):

    user_id = require_user(
        request
    )


    complete_goal(
        user_id,
        goal_id
    )


    return {
        "success": True,
        "message": "Goal completed."
    }


# ============================================================
# DELETE GOAL
# ============================================================

@app.delete("/api/goals/{goal_id}")
def remove_goal(
    request: Request,
    goal_id: int
):

    user_id = require_user(
        request
    )


    delete_goal(
        user_id,
        goal_id
    )


    return {
        "success": True,
        "message": "Goal deleted."
    }