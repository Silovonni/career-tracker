def calculate_project_score(projects):
    """
    Calculates a project score based on
    the number and status of projects.
    """

    if not projects:
        return 0

    score = 0

    for project in projects:

        status = project[4].lower()

        if status == "completed":
            score += 25

        elif status == "active":
            score += 15

        elif status == "planned":
            score += 5

    return min(score, 100)


def calculate_skill_score(skills):
    """
    Calculates a skill score based on
    skill count and proficiency level.
    """

    if not skills:
        return 0

    score = 0

    level_points = {
        "beginner": 10,
        "intermediate": 20,
        "advanced": 30,
        "expert": 40
    }

    for skill in skills:

        level = skill[2].lower()

        score += level_points.get(
            level,
            0
        )

    return min(score, 100)


def calculate_learning_score(study_hours):
    """
    Calculates a learning consistency score
    based on weekly study hours.
    """

    if study_hours >= 20:
        return 100

    elif study_hours >= 15:
        return 90

    elif study_hours >= 10:
        return 75

    elif study_hours >= 5:
        return 60

    elif study_hours > 0:
        return 35

    return 0


def calculate_portfolio_score(
    projects,
    skills
):
    """
    Calculates how developed the user's
    career portfolio is.
    """

    project_points = min(
        len(projects) * 10,
        50
    )

    skill_points = min(
        len(skills) * 10,
        50
    )

    return project_points + skill_points


def calculate_overall_progress(
    project_score,
    skill_score,
    learning_score,
    portfolio_score
):
    """
    Combines the major CareerOS metrics
    into one overall career progress score.
    """

    overall_score = (
        project_score * 0.30
        +
        skill_score * 0.30
        +
        learning_score * 0.20
        +
        portfolio_score * 0.20
    )

    return round(
        overall_score
    )


def determine_stage(score):
    """
    Determines the user's current
    career development stage.
    """

    if score >= 90:
        return "Career Ready"

    elif score >= 75:
        return "Advanced Builder"

    elif score >= 60:
        return "Developing Professional"

    elif score >= 40:
        return "Early Builder"

    elif score >= 20:
        return "Getting Started"

    return "Just Beginning"


def generate_recommendations(
    project_score,
    skill_score,
    learning_score,
    portfolio_score
):
    """
    Generates recommendations based
    on the user's weakest career areas.
    """

    recommendations = []


    if project_score < 60:

        recommendations.append(
            "Build and complete more projects "
            "to strengthen your portfolio."
        )


    if skill_score < 60:

        recommendations.append(
            "Continue developing technical "
            "skills and increase proficiency."
        )


    if learning_score < 60:

        recommendations.append(
            "Increase your weekly study time "
            "to build stronger learning consistency."
        )


    if portfolio_score < 60:

        recommendations.append(
            "Add more projects and skills "
            "to create a stronger professional profile."
        )


    if not recommendations:

        recommendations.append(
            "Your career development is progressing "
            "well. Focus on advanced projects and "
            "real-world experience."
        )


    return recommendations


def generate_career_report(
    study_hours,
    projects,
    skills
):
    """
    Generates a complete CareerOS analytics report.
    """

    project_score = calculate_project_score(
        projects
    )


    skill_score = calculate_skill_score(
        skills
    )


    learning_score = calculate_learning_score(
        study_hours
    )


    portfolio_score = calculate_portfolio_score(
        projects,
        skills
    )


    overall_score = calculate_overall_progress(
        project_score,
        skill_score,
        learning_score,
        portfolio_score
    )


    stage = determine_stage(
        overall_score
    )


    recommendations = generate_recommendations(
        project_score,
        skill_score,
        learning_score,
        portfolio_score
    )


    return {

        "overall_score":
            overall_score,

        "stage":
            stage,

        "metrics": {

            "projects":
                project_score,

            "skills":
                skill_score,

            "learning":
                learning_score,

            "portfolio":
                portfolio_score

        },

        "recommendations":
            recommendations

    }