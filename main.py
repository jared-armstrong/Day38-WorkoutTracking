from datetime import datetime
import requests
import os

APP_ID = "85909f4b"
API_KEY = "7d566d4ebab499170ee7d0af81c80c92"
BEARER_TOKEN = "BeArTh12T0K3NS1R"

GENDER = "Male"
WEIGHT_KG = 88.5
HEIGHT_CM = 179
AGE = 23

exercise_headers = {
    'Content-type': 'application/json',
    'x-app-id': APP_ID,
    'x-app-key': API_KEY
}

sheety_header = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"


exercise_text = input("Tell me which exercises you did: ")

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

exercise_response = requests.post(url=exercise_endpoint, json=parameters, headers=exercise_headers)
exercise_result = exercise_response.json()
print(exercise_response.status_code)
print(exercise_result)

exercise_type = exercise_result['exercises'][0]['name']
exercise_duration = exercise_result['exercises'][0]['duration_min']
exercise_calories = exercise_result['exercises'][0]['nf_calories']

sheet_endpoint = "https://api.sheety.co/66fbb1f64ef4d20996a30e4c61b28c2b/myWorkoutsDay38/workouts"

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in exercise_result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=sheety_header)

    print(sheet_response.text)
