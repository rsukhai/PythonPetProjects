
import requests
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC68913d293983f7ec3d5dfd4aecf241c6"
auth_token = "a056e3f0c73c30f6c78d5c4c4d37eea8"


api_key = "8846dc8f81099e58c9294f850559a4c7"
parameters = {
        "lat": "44.123947",
        "lon": "7.904663",
        "appid": api_key,
        "cnt":4
    }

response = requests.get(url=f"http://api.openweathermap.org/data/2.5/forecast",params=parameters)
response.raise_for_status()
data = response.json()
id_weather = data["list"][0]["weather"][0]["id"]
status = response.status_code

will_rain = False



for hour_fata in data["list"]:
    code = hour_fata["weather"][0]["id"]
    if code < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Візьми парасолю",
        from_="+12565024111",
        to="+380961043419",
    )
print(message.status)

print(id_weather)