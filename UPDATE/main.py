import os
from git import Repo
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
    if(response.json()["name"] != version["name"]):
        print("New update found, updating...")
        if os.path.exists(repo_local_path):
            repo = Repo(repo_local_path)
            repo.remotes.origin.pull()
        else:
            repo = Repo.clone_from(repo_url, repo_local_path)
        with open("../UPDATE/version.json", 'w') as f:
            json.dump(response.json(), f)
        print("Update done !")
    else:
        print("No update found.")
    print("Authenticating on Twitch...")
    exit(0)
except:
    print("Failed to get update data !")
    exit(-1)

