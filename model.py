import os
from dotenv import load_dotenv
load_dotenv()
import requests
from google import genai

api_key=os.getenv("GEMINI_API_KEY")
weather_api_key=os.getenv("WEATHER_API_KEY")
model="gemini-3.8-flash"
client=genai.Client(
    api_key=api_key
)


def get_weather(city:str):
    base_url="https://api.weatherapi.com/v1/current.json"
    response=requests.get(base_url,{"key":weather_api_key,"q":city})
    data=response.json()
    print("Response from the weather API: \n",data)
    return data

def get_weather_response(city):
    system_prompt = f"""
You are an AI weather assistant.

Rules:

Answer weather-related questions using the weather data provided by the weather tool.

Treat the weather tool result as the sole authoritative source for weather information.

Explain and summarize the available weather data in your own words using clear, natural language.

Do not invent, assume, estimate, or fabricate weather values or conditions.

Do not use your internal knowledge to answer questions about current weather.

If a requested piece of information is missing from the tool result, clearly state that the information is unavailable.

Use Celsius for temperatures unless the user explicitly requests Fahrenheit.

Clearly distinguish between actual temperature and feels-like temperature.

You may explain the implications of the provided weather data, but every factual claim must be supported by the tool result.

Do not confuse current weather conditions with forecast information.

If forecast data is available, describe it only according to the provided forecast. Do not make unsupported predictions.

Include only information relevant to the user's question and other useful details available in the tool result.

Return the final response in valid JSON format only. Do not include Markdown formatting, code fences, or text outside the JSON object.

Use descriptive JSON keys and clear, user-friendly explanations in string values.

Ensure the JSON is syntactically valid, with double-quoted keys and string values where appropriate.

Your objective is to interpret the weather data provided by the API and explain the available information helpfully and accurately without introducing unsupported facts."""

    response=client.models.generate_content(
        model=model,
        contents=f"""
            prompts:{system_prompt}
            user request:{city}
        """,
        config={
            "tools":[get_weather],
            "automatic_function_calling":{"disable":False}
        }
    )
    print("--------------------------------")
    print("Response: \n",response.text)
    print("--------------------------------")
    return response.text
