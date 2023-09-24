import csv
import random
import datetime
import time
import numpy as np
from sklearn.ensemble import IsolationForest

# Authorization Token
AUTHORIZED_TOKEN = "your_authorized_token_here"

# List of useful app names
USEFUL_APPS = [
    "Calendar", "Maps", "Weather", "Notes", "Calculator",
    "To-Do List", "Music Player", "News", "Fitness Tracker", "Recipe Book",
    "Language Learning", "Meditation Guide", "Budget Planner", "E-Book Reader",
    "Podcast Player", "Translator", "Flashlight", "File Manager", "Alarm Clock",
    "Scanner", "Photo Editor", "Video Player", "Password Manager", "Email Client",
]

def generate_synthetic_data():

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


# Class That analyze behavior of the user

class BehaviorAnalyzer:
    def __init__(self, baseline_data, initial_threshold=0.5, auth_token=None):
        self.anomaly_threshold = initial_threshold
        self.auth_token = auth_token
        self.model = self.build_model(baseline_data)

    def authenticate(self, auth_token):
        return auth_token == self.auth_token

    def build_model(self, data):
        # Extract features from data and fit Isolation Forest model
        app_usage_data = np.array(list(data.get("App Usage", {}).values()))
        location_patterns_data = np.array(list(data.get("Location Patterns", {}).values()))
        X_train = np.column_stack((app_usage_data, location_patterns_data))
        model = IsolationForest(contamination=self.anomaly_threshold)
        model.fit(X_train)
        return model


# Updated Code
    def analyze_behavior(self, current_data, auth_token=None):
        if auth_token and not self.authenticate(auth_token):
            print("Unauthorized access. Please provide a valid authentication token.")
            return

        if not self.is_valid_data(current_data):
            print("Invalid data format. Skipping analysis.")
            return

        app_usage = np.array(list(current_data.get("App Usage", {}).values()))
        location_patterns = np.array(list(current_data.get("Location Patterns", {}).values()))
        X_test = np.column_stack((app_usage, location_patterns))

        if self.model is None:
            print("Model not initialized. Please set the baseline data first.")
            return

        # Predict anomalies using the Isolation Forest model
        anomalies = self.model.predict(X_test)
        print("Anomalies are: ", anomalies)

        if -1 in anomalies:
            self.alert_user()
            

    def calculate_anomalies(self, baseline, current):
        total_anomalies = 0
        for app, baseline_usage in baseline.items():
            if app in current:
                current_usage = current[app]
                anomaly_score = abs(current_usage - baseline_usage) / baseline_usage
                total_anomalies += anomaly_score
        return total_anomalies

    def alert_user(self):
        print("Suspicious behavior detected! Please review your recent activity and take necessary actions.")

    def is_valid_data(self, data):
        print(type(data))
        if not isinstance(data, dict):
            
            return False
        print(data)
        for key in ["App Usage", "Location Patterns"]:
            if key not in data:
                return False
            if not isinstance(data[key], dict):
                return False

        return True

    def set_baseline(self, baseline_data, auth_token=None):
        if auth_token and not self.authenticate(auth_token):
            print("Unauthorized access. Please provide a valid authentication token.")
            return

        if not self.is_valid_data(baseline_data):
            print("Invalid baseline data format. Baseline setting failed.")
            return

        self.baseline_data = baseline_data
        self.model = self.build_model(baseline_data)

# Updated Code
    def update_baseline(self, new_baseline_data, auth_token=None):
        if auth_token and not self.authenticate(auth_token):
            print("Unauthorized access. Please provide a valid authentication token.")
            return

        if not self.is_valid_data(new_baseline_data):
            print("Invalid baseline data format. Baseline update failed.")
            return

        # Update baseline data and rebuild the model
        self.baseline_data = new_baseline_data
        self.model = self.build_model(new_baseline_data)

    def adjust_threshold(self, new_threshold, auth_token=None):
        if auth_token and not self.authenticate(auth_token):
            print("Unauthorized access. Please provide a valid authentication token.")
            return

        if 0 <= new_threshold <= 1:
            self.anomaly_threshold = new_threshold
            # Rebuild the model with the updated threshold
            self.model = self.build_model(self.baseline_data)
        else:
            print("Invalid threshold value. Threshold adjustment failed.")


# Example usage:
if __name__ == "__main__":
    generate_synthetic_data()

    # Load synthetic data from the generated CSV file
    synthetic_data = {}
    with open("synthetic_user_data.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            timestamp = row["Timestamp"]
            location_patterns = eval(row["Location Patterns"])
            app_usage = eval(row["App Usage"])
            synthetic_data[timestamp] = {"Location Patterns": location_patterns, "App Usage": app_usage}

    # Use the first 5 minutes of synthetic data as the baseline
    baseline_data = {}
    for timestamp in list(synthetic_data.keys())[:5]:
        baseline_data.update(synthetic_data[timestamp])

    # Set Baseline in the class BehaviorAnalyzer
    behavior_analyzer = BehaviorAnalyzer(baseline_data, auth_token=AUTHORIZED_TOKEN)

    while True:  # Simulating real-time monitoring (exit loop with Ctrl+C)
        # Simulate current data (use the next minute of synthetic data)
        current_data = synthetic_data[list(synthetic_data.keys())[5]]
        del synthetic_data[list(synthetic_data.keys())[0]]

        # Simulate unauthorized access by omitting the auth_token
        # behavior_analyzer.analyze_behavior(current_data)

        # Simulate authorized access by providing the correct auth_token
        behavior_analyzer.analyze_behavior(current_data, auth_token=AUTHORIZED_TOKEN)

        time.sleep(5)  #
