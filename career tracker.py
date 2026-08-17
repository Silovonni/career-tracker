def welcome():
    print()
    print("========================================")
    print("           CAREER TRACKER")
    print("========================================")
    print("Welcome to your career development tracker!")
    print()


def get_user_info():
    print("===== YOUR INFORMATION =====")

    name = input("What is your name? ").strip()

    while True:
        try:
            age = int(input("How old are you? "))

            if age > 0:
                break

            print("Please enter a valid age.")

        except ValueError:
            print("Please enter your age as a number.")

    career_goal = input(
        "What is your career goal? "
    ).strip()

    while True:
        try:
            study_hours = float(
                input(
                    "How many hours do you study Python each week? "
                )
            )

            if study_hours >= 0:
                break

            print("Study hours cannot be negative.")

        except ValueError:
            print("Please enter a number.")

    while True:
        try:
            projects_completed = int(
                input(
                    "How many projects have you completed so far? "
                )
            )

            if projects_completed >= 0:
                break

            print("Projects cannot be negative.")

        except ValueError:
            print("Please enter a whole number.")

    return (
        name,
        age,
        career_goal,
        study_hours,
        projects_completed
    )


def calculate_progress(study_hours):
    four_week_hours = study_hours * 4
    yearly_hours = study_hours * 52

    return four_week_hours, yearly_hours


def calculate_career_score(
    study_hours,
    projects_completed
):
    study_score = min(
        study_hours * 5,
        50
    )

    project_score = min(
        projects_completed * 10,
        50
    )

    total_score = round(
        study_score + project_score
    )

    return total_score


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


def display_progress(
    name,
    age,
    career_goal,
    study_hours,
    projects_completed,
    four_week_hours,
    yearly_hours,
    career_score,
    career_level
):
    print()
    print("========================================")
    print("           YOUR CAREER PROFILE")
    print("========================================")

    print("Name:", name)
    print("Age:", age)
    print("Career Goal:", career_goal)
    print(
        "Python Study Hours Per Week:",
        study_hours
    )
    print(
        "Projects Completed:",
        projects_completed
    )
    print(
        "Study Hours Over 4 Weeks:",
        four_week_hours
    )
    print(
        "Projected Study Hours Per Year:",
        yearly_hours
    )

    print()
    print("Career Score:", career_score, "/ 100")
    print("Career Level:", career_level)


def assess_progress(
    study_hours,
    projects_completed
):
    print()
    print("========================================")
    print("             ASSESSMENT")
    print("========================================")

    if study_hours >= 15:
        print(
            "Excellent! You are putting serious "
            "time into Python."
        )

    elif study_hours >= 10:
        print(
            "Good work! You are building a solid "
            "study habit."
        )

    elif study_hours >= 5:
        print(
            "You're getting started. Try to gradually "
            "increase your study time."
        )

    else:
        print(
            "Try to dedicate more time to Python "
            "each week."
        )

    print()

    if projects_completed >= 10:
        print(
            "Excellent portfolio progress. "
            "You are building serious project experience."
        )

    elif projects_completed >= 5:
        print(
            "Great! You are building a strong "
            "project portfolio."
        )

    elif projects_completed >= 1:
        print(
            "Good start! Keep building projects."
        )

    else:
        print(
            "You haven't completed a project yet."
        )


def show_goals(
    study_hours,
    projects_completed
):
    print()
    print("========================================")
    print("              NEXT STEPS")
    print("========================================")

    if study_hours < 10:
        print(
            "Goal: Reach at least 10 Python "
            "study hours per week."
        )
    else:
        print(
            "Study goal: On track."
        )

    if projects_completed < 5:
        print(
            "Goal: Build at least 5 portfolio projects."
        )
    else:
        print(
            "Project goal: On track."
        )

    print(
        "Keep learning, building, testing, "
        "and documenting your work."
    )


def main():
    welcome()

    (
        name,
        age,
        career_goal,
        study_hours,
        projects_completed
    ) = get_user_info()

    (
        four_week_hours,
        yearly_hours
    ) = calculate_progress(
        study_hours
    )

    career_score = calculate_career_score(
        study_hours,
        projects_completed
    )

    career_level = get_career_level(
        career_score
    )

    display_progress(
        name,
        age,
        career_goal,
        study_hours,
        projects_completed,
        four_week_hours,
        yearly_hours,
        career_score,
        career_level
    )

    assess_progress(
        study_hours,
        projects_completed
    )

    show_goals(
        study_hours,
        projects_completed
    )

    while True:

        print()
        print("========================================")
        print("                MENU")
        print("========================================")
        print("1. View Career Profile")
        print("2. View Assessment")
        print("3. View Next Steps")
        print("4. Recalculate Career Score")
        print("5. Exit")

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":

            display_progress(
                name,
                age,
                career_goal,
                study_hours,
                projects_completed,
                four_week_hours,
                yearly_hours,
                career_score,
                career_level
            )

        elif choice == "2":

            assess_progress(
                study_hours,
                projects_completed
            )

        elif choice == "3":

            show_goals(
                study_hours,
                projects_completed
            )

        elif choice == "4":

            career_score = calculate_career_score(
                study_hours,
                projects_completed
            )

            career_level = get_career_level(
                career_score
            )

            print()
            print(
                "Career Score:",
                career_score,
                "/ 100"
            )

            print(
                "Career Level:",
                career_level
            )

        elif choice == "5":

            print()
            print(
                "Thanks for using Career Tracker."
            )
            print(
                "Keep building. Keep learning."
            )
            print()

            break

        else:

            print(
                "Invalid choice. Please choose "
                "an option from 1 to 5."
            )


if __name__ == "__main__":
    main()