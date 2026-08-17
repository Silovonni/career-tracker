from database import (
    create_tables,
    add_user,
    get_user,
    add_project,
    get_projects,
    add_skill,
    get_skills
)

from career_score import (
    calculate_career_score,
    get_career_level,
    get_career_message
)

from analytics import (
    generate_career_report,
    display_career_report
)


def create_career_profile():
    print()
    print("===== CREATE CAREER PROFILE =====")

    name = input("Name: ").strip()

    while True:
        try:
            age = int(input("Age: "))

            if age > 0:
                break

            print("Age must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")

    career_goal = input("Career goal: ").strip()

    while True:
        try:
            study_hours = float(
                input("Python study hours per week: ")
            )

            if study_hours >= 0:
                break

            print("Study hours cannot be negative.")

        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            projects_completed = int(
                input("Projects completed: ")
            )

            if projects_completed >= 0:
                break

            print("Projects cannot be negative.")

        except ValueError:
            print("Please enter a whole number.")

    user_id = add_user(
        name,
        age,
        career_goal,
        study_hours,
        projects_completed
    )

    print()
    print("Career profile created!")
    print(f"Your CareerOS user ID is {user_id}.")

    return user_id


def show_profile(user_id):
    user = get_user(user_id)

    print()
    print("==============================")
    print("        CAREER PROFILE")
    print("==============================")

    if user is None:
        print("Profile not found.")
        return

    print("ID:", user[0])
    print("Name:", user[1])
    print("Age:", user[2])
    print("Career Goal:", user[3])
    print("Study Hours:", user[4])
    print("Projects Completed:", user[5])
    print("Created:", user[6])


def create_project(user_id):
    print()
    print("===== ADD PROJECT =====")

    name = input("Project name: ").strip()

    description = input(
        "Project description: "
    ).strip()

    technology = input(
        "Technology used: "
    ).strip()

    status = input(
        "Status (planned/active/completed): "
    ).strip().lower()

    if status not in (
        "planned",
        "active",
        "completed"
    ):
        status = "planned"

    project_id = add_project(
        user_id,
        name,
        description,
        technology,
        status
    )

    print()
    print(f"Project created with ID {project_id}.")


def show_projects(user_id):
    projects = get_projects(user_id)

    print()
    print("==============================")
    print("         YOUR PROJECTS")
    print("==============================")

    if not projects:
        print("No projects yet.")
        return

    for project in projects:
        print()
        print("Project ID:", project[0])
        print("Name:", project[1])
        print("Description:", project[2])
        print("Technology:", project[3])
        print("Status:", project[4])
        print("Created:", project[5])


def create_skill(user_id):
    print()
    print("===== ADD SKILL =====")

    name = input(
        "Skill name: "
    ).strip()

    level = input(
        "Skill level "
        "(beginner/intermediate/advanced): "
    ).strip().lower()

    if level not in (
        "beginner",
        "intermediate",
        "advanced"
    ):
        level = "beginner"

    skill_id = add_skill(
        user_id,
        name,
        level
    )

    print()
    print(f"Skill created with ID {skill_id}.")


def show_skills(user_id):
    skills = get_skills(user_id)

    print()
    print("==============================")
    print("          YOUR SKILLS")
    print("==============================")

    if not skills:
        print("No skills yet.")
        return

    for skill in skills:
        print()
        print("Skill ID:", skill[0])
        print("Name:", skill[1])
        print("Level:", skill[2])
        print("Added:", skill[3])


def show_career_score(user_id):
    user = get_user(user_id)

    if user is None:
        print("Profile not found.")
        return

    projects = get_projects(user_id)
    skills = get_skills(user_id)

    study_hours = user[4]

    projects_completed = len(projects)
    skills_completed = len(skills)

    score = calculate_career_score(
        study_hours,
        projects_completed,
        skills_completed
    )

    level = get_career_level(score)

    message = get_career_message(score)

    print()
    print("==============================")
    print("         CAREER SCORE")
    print("==============================")

    print("Career Score:", score, "/ 100")
    print("Career Level:", level)

    print()
    print(message)


def show_career_analytics(user_id):
    user = get_user(user_id)

    if user is None:
        print("Profile not found.")
        return

    projects = get_projects(user_id)
    skills = get_skills(user_id)

    study_hours = user[4]

    report = generate_career_report(
        study_hours,
        projects,
        skills
    )

    display_career_report(report)


def show_menu():
    print()
    print("==============================")
    print("        CAREEROS MENU")
    print("==============================")
    print("1. View Career Profile")
    print("2. Add Project")
    print("3. View Projects")
    print("4. Add Skill")
    print("5. View Skills")
    print("6. View Career Score")
    print("7. View Career Analytics")
    print("8. Exit")


def main():
    create_tables()

    print()
    print("================================")
    print("           CAREEROS")
    print("================================")
    print("Your Career Development System")

    user_id = create_career_profile()

    while True:
        show_menu()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            show_profile(user_id)

        elif choice == "2":
            create_project(user_id)

        elif choice == "3":
            show_projects(user_id)

        elif choice == "4":
            create_skill(user_id)

        elif choice == "5":
            show_skills(user_id)

        elif choice == "6":
            show_career_score(user_id)

        elif choice == "7":
            show_career_analytics(user_id)

        elif choice == "8":
            print()
            print("Thanks for using CareerOS.")
            print("Keep building. Keep learning.")
            break

        else:
            print()
            print("Invalid option. Please choose 1-8.")


if __name__ == "__main__":
    main()