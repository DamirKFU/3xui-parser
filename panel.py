import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("PANEL_URL") + os.getenv("PANEL_PATH")

USERNAME = os.getenv("PANEL_USERNAME")
PASSWORD = os.getenv("PANEL_PASSWORD")

session = requests.Session()


def login():
    url = f"{BASE}/login"

    data = {
        "username": USERNAME,
        "password": PASSWORD
    }

    session.post(url, data=data, verify=False)


def get_inbounds():
    url = f"{BASE}/panel/api/inbounds/list"

    r = session.get(url, verify=False)
    return r.json()


def reset_traffic():
    url = f"{BASE}/panel/api/inbounds/resetAllTraffics"

    r = session.post(url, verify=False)
    return r.json()