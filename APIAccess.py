import requests
import json

# Replace these with your Canvas instance details
API_URL = "https://canvas.instructure.com/api/v1"
ACCESS_TOKEN = "2096~3xDL4HuFn7ywFTn2MDXYEPJZwvuVWHC3kK4AZAFTGUxEL74HGvzYPXDuw7xKmvYU"

# Function to make API requests
def get_canvas_data(endpoint):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(f"{API_URL}/{endpoint}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Example: Get a list of courses
def get_courses():
    return get_canvas_data("courses")

# Example Usage
if __name__ == "__main__":
    courses = get_courses()
    if courses:
        for course in courses:
            print(f"Course: {course['name']} (ID: {course['id']})")
