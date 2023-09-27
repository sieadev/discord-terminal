import json, requests


def Start(session: requests.Session, email: str, password: str) -> tuple:
    fingerprint = Fingerprint(session)
    Cookies(session)
    token = Login(session, email, password, fingerprint)
    return fingerprint, token


def StartWithToken(session: requests.Session, token: str) -> str:
    fingerprint = Fingerprint(session)
    Cookies(session)
    if getUsername(session, token) is "None":
        return "None"
    else:
        return fingerprint


def Fingerprint(session: requests.Session):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.180 Safari/537.36',
        'X-Track': 'eyJvcyI6IklPUyIsImJyb3dzZXIiOiJTYWZlIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKElQaG9uZTsgQ1BVIEludGVybmFsIFByb2R1Y3RzIFN0b3JlLCBhcHBsaWNhdGlvbi8yMDUuMS4xNSAoS0hUTUwpIFZlcnNpb24vMTUuMCBNb2JpbGUvMTVFMjQ4IFNhZmFyaS82MDQuMSIsImJyb3dzZXJfdmVyc2lvbiI6IjE1LjAiLCJvc192IjoiIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfZG9tYWluX2Nvb2tpZSI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOiJzdGFibGUiLCJjbGllbnRfZXZlbnRfc291cmNlIjoic3RhYmxlIn0',
    }

    response = session.get('https://discord.com/api/v9/experiments', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["fingerprint"]
    else:
        return None


def Cookies(session: requests.Session):
    r = session.get("https://discord.com")
    if "Grab a seat in a voice channel" in r.text:
        return 200
    else:
        return 404


def Login(session: requests.Session, email: str, password: str, fingerprint: str):
    headers = {
        "authority": "discord.com",
        "method": "POST",
        "path": "/api/v9/auth/login",
        "scheme": "https",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Length": "124",
        "Content-Type": "application/json",
        "Origin": "https://discord.com",
        "Referer": "https://discord.com/login",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.180 Safari/537.36",
        "X-Debug-Options": "bugReporterEnabled",
        "X-Discord-Locale": "de",
        "X-Discord-Timezone": "Europe/Berlin",
        "X-Fingerprint": f"{fingerprint}",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImRlLURFIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNi4wLjU4NDUuMTgwIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMTYuMC41ODQ1LjE4MCIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6Ind3dy5nb29nbGUuY29tIiwic2VhcmNoX2VuZ2luZV9jdXJyZW50IjoiZ29vZ2xlIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjMwNjU2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    payload = {
        "login": email,
        "password": password,
        "undelete": False,
        "login_source": None,
        "gift_code_sku_id": None
    }
    r = session.post("https://discord.com/api/v9/auth/login", headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        return r.json()['token']
    else:
        if "retry_after" in r.text:
            return "Ratelimit", r.json()['retry_after']
        else:
            return "Couldn't recieve Token because of unkown error", r.text


def getUsername(session: requests.Session, token: str) -> str:
    # Get Username
    h = {"Authorization": token}
    r = session.get("https://discord.com/api/v9/users/@me", headers=h)
    if r.status_code == 200:
        return r.json()['username']
    elif r.status_code == 401:
        return "Token not Authorization"
    return "None"
