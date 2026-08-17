def calculate_study_score(study_hours):
    score = study_hours * 5

    if score > 50:
        score = 50

    return round(score)


def calculate_project_score(projects_completed):
    score = projects_completed * 10

    if score > 50:
        score = 50

    return round(score)


def calculate_skill_score(skills_completed):
    score = skills_completed * 10

    if score > 50:
        score = 50

    return round(score)


def calculate_career_score(
    study_hours,
    projects_completed,
    skills_completed
):
    study_score = calculate_study_score(
        study_hours
    )

    project_score = calculate_project_score(
        projects_completed
    )

    skill_score = calculate_skill_score(
        skills_completed
    )

    total_score = (
        study_score
        + project_score
        + skill_score
    )

    final_score = round(
        total_score / 1.5
    )

    return final_score


def get_career_level(score):

    if score >= 90:
        return "Elite"

    elif score >= 75:
        return "Advanced"

    elif score >= 50:
        return "Developing"

    elif score >= 25:
        return "Beginner"

    else:
        return "Getting Started"


def get_career_message(score):

    if score >= 90:
        return (
            "You are operating at a very high "
            "level. Focus on advanced projects, "
            "real-world experience, and leadership."
        )

    elif score >= 75:
        return (
            "You are making strong progress. "
            "Focus on improving your portfolio "
            "and gaining professional experience."
        )

    elif score >= 50:
        return (
            "You have a solid foundation. "
            "Keep building projects and expanding "
            "your technical skills."
        )

    elif score >= 25:
        return (
            "You are developing your foundation. "
            "Consistency is the key right now."
        )

    else:
        return (
            "You are at the beginning of your "
            "journey. Start building and learning."
        )


def display_career_score(
    study_hours,
    projects_completed,
    skills_completed
):

    score = calculate_career_score(
        study_hours,
        projects_completed,
        skills_completed
    )

    level = get_career_level(
        score
    )

    message = get_career_message(
        score
    )

    print()
    print("==============================")
    print("       CAREER SCORE")
    print("==============================")

    print(
        "Score:",
        score,
        "/ 100"
    )

    print(
        "Level:",
        level
    )

    print()
    print(message)

    return score