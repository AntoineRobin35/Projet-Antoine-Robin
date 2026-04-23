from google import genai
import requests


give_weather = {
    "name": "give_weather",
    "description": "A tool for search the today's weather",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Choose the city you want"
            },
            "hour": {
                "type": "integer",
                "minimum": 0,
                "maximum": 23,
                "description": "Choose for what hour you want the weather between 0 and 23"
            }
        },
        "required": ["city", "hour"]
    }
}

give_people = {
    "name": "give_people",
    "description": "a tool to search how many people live in which city in which year",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "enum": ["Guignen", "Guichen", "Baulon", "Goven", "lassy"],
                "description": "choose the city you want the people's number"
            },
            "year": {
                "type": "integer",
                "description": "choose the year you want the people's number"
            }
        },
    "required": ["city", "year"]
    }
}
def get_weather(city: str, hour: int) -> dict[str, int]:
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    data = response.json()
    return {"city": city, "hour": hour, "temperature": data["weather"][0]["hourly"][hour//3]}

def get_people(city: str, year: int) -> dict[str, int]:
    if city == "Guignen":
        return {"city": city, "year": year, "habitant": year * 2}
    elif city == "Guichen":
        return {"city": city, "year": year, "habitant": year * 3}
    elif city == "Baulon":
        return {"city": city, "year": year, "habitant": year * 4}
    elif city == "Goven":
        return {"city": city, "year": year, "habitant": year * 5}
    elif city == "Lassy":
        return {"city": city, "year": year, "habitant": year * 6}

client = genai.Client(api_key="Clé api")
chat = client.chats.create(model="gemini-2.5-flash", config=genai.types.GenerateContentConfig(
    system_instruction="Lorsque tu as besoin de donner la méteo, utilise la fonction get_weather. "
                       "Lorsque tu as besoins de donner le nombre de personne d'une ville utilise la fonction get_people",
    tools=[genai.types.Tool(function_declarations=([give_weather, give_people]))]
))
tour = 0
while True:
    response = chat.send_message(message=input("Entrer votre prompt"))
    if response.candidates[0].content.parts[0].function_call is not None:
        tour += 1
        if tour >= 10:
            print("Stop, Trop de tour")
            break

        for parts in response.candidates[0].content.parts:
            args = parts.function_call.args
            name = parts.function_call.name

            results = None
            if name == "give_people":
                results = get_people(args["city"], args["year"])
            elif name == "give_weather":
                results = get_weather(args["city"], args["hour"])


            response = chat.send_message(
                genai.types.Part(
                    function_response=genai.types.FunctionResponse(
                        name=name,
                        response=results,
                    )
                )
            )

    print(response.text)