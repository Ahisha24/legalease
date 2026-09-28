from google import genai


API_KEY = "AIzaSyC0hzoM6zhOb0loRF91dC5mpa_euzvYLuU"

try:
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Hi",
    )
    print("SUCCESS! Output:", response.text)
except Exception as e:
    print("ERROR DETAILS:", e)