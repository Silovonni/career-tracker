print("===== CAREER TRACKER =====")

name = input("What is your name? ")
age = int(input("How old are you? "))
career_goal = input("What is your career goal? ")
study_hours = int(input("How many hours do you study Python each week? "))
projects_completed = int(input("How many projects have you completed so far? "))

four_week_hours = study_hours * 4

print()
print("===== YOUR PROGRESS =====")
print("Name:", name)
print("Age:", age)
print("Career Goal:", career_goal)
print("Python Study Hours Per Week:", study_hours)
print("Projects Completed:", projects_completed)
print("Study Hours Over 4 Weeks:", four_week_hours)

print()
print("===== ASSESSMENT =====")

if study_hours >= 15:
    print("Excellent! You are putting serious time into Python.")
elif study_hours >= 10:
    print("Good work! You are building a solid study habit.")
elif study_hours >= 5:
    print("You're getting started. Try to gradually increase your study time.")
else:
    print("You should try to dedicate more time to Python each week.")

if projects_completed >= 5:
    print("Great! You are building a strong project portfolio.")
elif projects_completed >= 1:
    print("Good start! Keep building projects.")
else:
    print("You haven't completed a project yet. This Career Tracker can be your first!")

while True:
    print()
    print("===== MENU =====")
    print("1. View Progress")
    print("2. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        print()
        print("===== YOUR PROGRESS =====")
        print("Name:", name)
        print("Age:", age)
        print("Career Goal:", career_goal)
        print("Python Study Hours Per Week:", study_hours)
        print("Projects Completed:", projects_completed)
        print("Study Hours Over 4 Weeks:", four_week_hours)

    elif choice == "2":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please choose 1 or 2.")