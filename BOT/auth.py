import requests
import json
import os
from datetime import datetime, timedelta
import os
from webbrowser import open_new_tab
from flask import Flask, render_template, request
from threading import Thread
from dotenv import load_dotenv
load_dotenv()
import logging

logging.getLogger('werkzeug').disabled = True

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
redirect_uri = "http://localhost:6969"  # Remplacez ceci par votre URL de redirection
token_file = "DATASTORE/connect.json"
access_token = None

def get_access_token():
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            token_data = json.load(f)
            expires_at = token_data.get("expires_at")
            if expires_at and datetime.utcnow() < datetime.utcfromtimestamp(expires_at):
                return token_data.get("access_token")
            else:
                return refresh_access_token(token_data.get("refresh_token"))
    return None

def save_access_token(access_token, expires_in):
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
    token_data = {"access_token": access_token, "expires_at": expires_at.timestamp()}
    with open(token_file, 'w') as f:
        json.dump(token_data, f)

def refresh_access_token(refresh_token):
    token_url = "https://id.twitch.tv/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()
    new_access_token = token_data.get("access_token")
    if new_access_token:
        expires_in = token_data.get("expires_in", 3600)  # Default expiration time is 1 hour
        save_access_token(new_access_token, expires_in)
        return new_access_token
    return None

def authenticate():
    access_token = get_access_token()

    if access_token:
        return access_token
    else:
        SRV_THREAD.start()
        auth_url = f"https://id.twitch.tv/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=chat:read+chat:edit"
        open_new_tab(auth_url)
        print(f"Ouverture du navigateur, en cas de problèmes voici le lien :\n{auth_url}")
        SRV_THREAD.join(15)


    



def SRV():
    app = Flask(__name__)
    @app.route("/")
    def get_code():
        client_id = os.environ['CLIENT_ID']
        client_secret = os.environ['CLIENT_SECRET']
        redirect_uri = "http://localhost:6969"  # Remplacez ceci par votre URL de redirection
        token_file = "DATASTORE/connect.json"
        access_token = None
        code = request.args.get('code')
        token_url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
        response = requests.post(token_url, data=data)
        token_data = response.json()
        access_token = token_data.get("access_token")
        if access_token:
            expires_in = token_data.get("expires_in", 3600)  # Default expiration time is 1 hour
            save_access_token(access_token, expires_in)
        return render_template("index.html")
    app.run(port=6969)

SRV_THREAD = Thread(target=SRV)
SRV_THREAD.daemon = True

def main():
    authenticate()    

if __name__ == "__main__":
    main()
