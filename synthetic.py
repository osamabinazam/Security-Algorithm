import csv
import random
import datetime

# List of useful app names
USEFUL_APPS = [
    "Calendar", "Maps", "Weather", "Notes", "Calculator",
    "To-Do List", "Music Player", "News", "Fitness Tracker", "Recipe Book",
    "Language Learning", "Meditation Guide", "Budget Planner", "E-Book Reader",
    "Podcast Player", "Translator", "Flashlight", "File Manager", "Alarm Clock",
    "Scanner", "Photo Editor", "Video Player", "Password Manager", "Email Client",
]

def generate_random_location_patterns():
    return {
        "Home": random.randint(30, 180),
        "Work": random.randint(60, 600),
        "Gym": random.randint(20, 120),
        "School": random.randint(120, 240),
        "Restaurant": random.randint(30, 120),
    }

def generate_synthetic_user_data():
    location_patterns = generate_random_location_patterns()
    app_usage = {
        app_name: random.randint(1, 200) for app_name in random.sample(USEFUL_APPS, 5)
    }
    permissions = {
        "Location": random.choice([True, False]),
        "Camera": random.choice([True, False]),
        "Contacts": random.choice([True, False]),
    }
    return location_patterns, app_usage, permissions

# Save data to a CSV file
csv_file = "synthetic_user_data.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Timestamp", "Location Patterns", "App Usage", "Permissions"])

    for minute in range(24*60):
        timestamp = datetime.datetime(2023, 8, 1, minute // 60, minute % 60).isoformat()
        location_patterns, app_usage, permissions = generate_synthetic_user_data()

        row_data = ["User", timestamp, location_patterns, app_usage, permissions]
        writer.writerow(row_data)

print(f"CSV file '{csv_file}' with synthetic user data for each minute has been created.")
