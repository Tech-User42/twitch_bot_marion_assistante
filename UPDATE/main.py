import os
from time import sleep
import json
import requests

repo_local_path = "../"
repo_url = "https://github.com/Tech-User42/twitch_bot_marion_assistante"

try:
    response = requests.get("https://api.github.com/repos/Tech-User42/twitch_bot_marion_assistante/releases/latest")
    try:
        with open("../UPDATE/version.json", 'r') as f:
            version = json.load(f)
    except:
        version = {
            "name": 1.0
        }
    print("Latest version : "+response.json()["name"])
    if(response.json()["name"] != version["name"]):
        print("There is a new update you can download it here : https://github.com/Tech-User42/twitch_bot_marion_assistante")
        sleep(7)
    else:
        print("Already up to date !")
    print("Authenticating on Twitch...")
    exit(0)
except Exception as E:
    print("Failed to get update data !")
    exit(-1)
