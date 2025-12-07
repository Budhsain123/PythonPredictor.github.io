import requests
import hashlib
import json
import time
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()

# ============================
# AUTO LOGIN CREDENTIALS
# ============================
AUTO_USERNAME = "918091245693"
AUTO_PASSWORD = "ziddiff143"

LOGIN_URL = "https://91clubapi.com/api/webapi/Login"
TEAM_DAY_URL = "https://91clubapi.com/api/webapi/TeamDayReport"


# SIGNATURE FUNCTIONS
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
    # They accept ANY string; using hex for safety
    return os.urandom(16).hex()


def make_signature(payload):
    return hashlib.md5(payload.encode()).hexdigest().upper()


# AUTO LOGIN
def auto_login():
    language = 0
    logintype = "mobile"
    phonetype = 1

    random_str = generate_random32()
    timestamp = str(int(time.time()))

    signature = generate_login_signature(
        language, logintype, phonetype, AUTO_PASSWORD, random_str, AUTO_USERNAME
    )

    payload = {
        "language": language,
        "logintype": logintype,
        "phonetype": phonetype,
        "pwd": AUTO_PASSWORD,
        "random": random_str,
        "timestamp": timestamp,
        "signature": signature,
        "username": AUTO_USERNAME
    }

    r = requests.post(LOGIN_URL, json=payload)

    try:
        return r.json()["data"]["token"]
    except:
        print("Login failed:", r.text)
        return None


# TEAM DAY REPORT (via proxy)
def team_day_report(uid):
    token = auto_login()
    if not token:
        return {"error": "Login failed"}

    day = time.strftime("%Y-%m-%d")
    language = 0
    lv = -1
    pageNo = 1
    pageSize = 10

    random_str = generate_random12()
    timestamp = int(time.time())

    payload_str = (
        f'{{"day":"{day}","language":{language},"lv":{lv},"pageNo":{pageNo},'
        f'"pageSize":{pageSize},"random":"{random_str}","userId":{uid}}}'
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
        "timestamp": timestamp,
        "userId": int(uid)
    }

    headers = {
        "Host": "91clubapi.com",
        "authorization": f"Bearer {token}",
        "sec-ch-ua-platform": "\"Android\"",
        "content-type": "application/json"
    }

    res = requests.post(TEAM_DAY_URL, json=body, headers=headers)

    try:
        data = res.json()["data"]["list"]
    except:
        return {"error": "Response error", "details": res.text}

    if not data:
        return {"error": "This user is not registered with NextWinAi's Referral Link"}

    return data


# PUBLIC API
@app.get("/get-data")
def api(uid: int):
    result = team_day_report(uid)
    return JSONResponse(result)