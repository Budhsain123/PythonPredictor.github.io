from fastapi import FastAPI
import requests
import hashlib
import time
import os
import json

app = FastAPI()

# ============================
# AUTO LOGIN CREDENTIALS
# ============================
AUTO_USERNAME = "918091245693"
AUTO_PASSWORD = "ziddiff143"

LOGIN_URL = "https://91clubapi.com/api/webapi/Login"
TEAM_DAY_URL = "https://91clubapi.com/api/webapi/TeamDayReport"


# LOGIN SIGNATURE
def generate_login_signature(language, logintype, phonetype, pwd, random_str, username):
    shonustr = (
        f'{{"language":{language},"logintype":"{logintype}","phonetype":{phonetype},'
        f'"pwd":"{pwd}","random":"{random_str}","username":"{username}"}}'
    )
    signature = hashlib.md5(shonustr.encode()).hexdigest().upper()
    return signature


def generate_random32():
    return os.urandom(16).hex()


def generate_random12():
    return os.urandom(16).hex()


def make_signature(payload):
    return hashlib.md5(payload.encode()).hexdigest().upper()


# AUTO LOGIN
def auto_login():
    username = AUTO_USERNAME
    password = AUTO_PASSWORD

    language = 0
    logintype = "mobile"
    phonetype = 1

    random_str = generate_random32()
    timestamp = str(int(time.time()))

    signature = generate_login_signature(
        language, logintype, phonetype, password, random_str, username
    )

    payload = {
        "language": language,
        "logintype": logintype,
        "phonetype": phonetype,
        "pwd": password,
        "random": random_str,
        "timestamp": timestamp,
        "signature": signature,
        "username": username
    }

    print("🔹 DEBUG: Sending Login Request")
    print("URL:", LOGIN_URL)
    print("Payload:", json.dumps(payload, indent=2))

    try:
        res = requests.post(LOGIN_URL, json=payload, timeout=15)
    except Exception as e:
        print("❌ Request failed:", str(e))
        return None

    print("🔹 DEBUG: Response Status Code:", res.status_code)
    print("🔹 DEBUG: Response Body:", res.text)

    try:
        token = res.json()["data"]["token"]
        print("✅ Login successful! Token:", token)
        return token
    except KeyError:
        print("❌ Login failed: Token not found in response")
        return None
    except Exception as e:
        print("❌ Login failed with exception:", str(e))
        return None


# TEAM DAY REPORT
def fetch_team_day(bearer_token, userId):
    day = time.strftime("%Y-%m-%d")
    language = 0
    lv = -1
    pageNo = 1
    pageSize = 10

    random_str = generate_random12()
    timestamp = int(time.time())

    if userId:
        payload_str = (
            f'{{"day":"{day}","language":{language},"lv":{lv},"pageNo":{pageNo},'
            f'"pageSize":{pageSize},"random":"{random_str}","userId":{userId}}}'
        )
    else:
        payload_str = (
            f'{{"day":"{day}","language":{language},"lv":{lv},"pageNo":{pageNo},'
            f'"pageSize":{pageSize},"random":"{random_str}"}}'
        )

    signature = make_signature(payload_str)

    body = {
        "day": day,
        "language": language,
        "lv": lv,
        "pageNo": pageNo,
        "pageSize": pageSize,
        "random": random_str,
        "signature": signature,
        "timestamp": timestamp
    }
    if userId:
        body["userId"] = int(userId)

    headers = {
        "Host": "91clubapi.com",
        "authorization": f"Bearer {bearer_token}",
        "sec-ch-ua-platform": "\"Android\"",
        "content-type": "application/json"
    }

    response = requests.post(TEAM_DAY_URL, headers=headers, json=body)

    try:
        return response.json()
    except:
        return {"error": "Bad response", "raw": response.text}


# ============================
# API ENDPOINT (Render)
# ============================

@app.get("/")
def home(uid: str = None):
    if uid is None:
        return {"error": "UID missing. Use ?uid=12345"}

    token = auto_login()
    if token is None:
        return {"error": "Login failed"}

    data = fetch_team_day(token, uid)
    return data