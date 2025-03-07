import requests
import openai
from datetime import datetime, timedelta

# Canvas API Credentials
API_URL = "https://canvas.instructure.com/api/v1"
ACCESS_TOKEN = "2096~3xDL4HuFn7ywFTn2MDXYEPJZwvuVWHC3kK4AZAFTGUxEL74HGvzYPXDuw7xKmvYU"

# OpenAI API Key
OPENAI_API_KEY = "yosk-proj-saWkxt178-j0ZsRogxWaR_wv4_7aPwOTBhSSeCkiogTFgnA4_t15Xq85yJdY_bOFTy3ne578EGT3BlbkFJUCjZSzey9_rhgaFL6ftKd_9xhFbwK7w_xKzaHqZilj4WQQPsTikcZTqRFYAFkAuByrLjQJougA"

# Function to get all courses for the user
# Function to make API requests
def get_canvas_data(endpoint):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    all_data = []
    url = f"{API_URL}/{endpoint}?per_page=100"  # Increase per_page to get more results

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            all_data.extend(data)
            
            # Check if there is another page
            if "next" in response.links:
                url = response.links["next"]["url"]
            else:
                url = None
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    return all_data

# Example: Get a list of courses
def get_courses():
    return get_canvas_data("courses")

def get_assignments():
    courses = get_courses()
    assignmentDictionary = {}
    for x in courses:
        course_id = x["id"]
        assignments = get_canvas_data(f"courses/{course_id}/assignments")
        for assignment in assignments:
            if(assignment["due_at"] != None):
                if course_id in assignmentDictionary:
                    assignmentDictionary[course_id].append((assignment["name"], assignment["due_at"]))
                else:
                    assignmentDictionary[course_id] = [(assignment["name"], assignment["due_at"])]

    return assignmentDictionary

assignmentDictionary = get_assignments()

# # Function to get suggested start date from OpenAI
# def get_suggested_start_date(assignment_name, due_date):
#     prompt = f"Given that the assignment '{assignment_name}' is due on {due_date}, suggest an appropriate start date considering workload and optimal study habits. Provide only the date in YYYY-MM-DD format."

#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         key=OPENAI_API_KEY,
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=20
#     )
    
#     return response["choices"][0]["message"]["content"].strip()

# # Function to create the full assignment schedule
# def create_full_schedule():
#     courses = get_courses()
#     full_schedule = {}

#     for course in courses:
#         course_name = course["name"]
#         course_id = course["id"]
#         assignments = get_canvas_assignments(course_id)

#         course_schedule = {}
#         for assignment in assignments:
#             name = assignment["name"]
#             due_date = assignment.get("due_at")  # Example: "2025-03-15T23:59:00Z"

#             if due_date:
#                 due_date_formatted = datetime.strptime(due_date, "%Y-%m-%dT%H:%M:%SZ").date()
#                 suggested_start_date = get_suggested_start_date(name, due_date_formatted)

#                 course_schedule[name] = [suggested_start_date, str(due_date_formatted)]

#         if course_schedule:
#             full_schedule[course_name] = course_schedule

#     return full_schedule

# # Run script
# if __name__ == "__main__":
#     schedule = create_full_schedule()
#     print(schedule)