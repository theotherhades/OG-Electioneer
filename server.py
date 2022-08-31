import requests, json, os

url = os.environ["SERVER_URL"]

def ping():
    """
    Wake the server to prevent long loadtimes for requests
    """
    try:
        requests.get(f"{url}/ping", timeout = 10)
        return "success"
    except requests.exceptions.Timeout:
        return "failure: ping request timed out"

def get_count(candidate: str = ""):
    """
    Get current vote count for <candidate>
    """
    r = json.loads(requests.get(f"{url}/count").text)

    if candidate == "" or candidate in r.keys():
        return r

    else:
        return "failure: candidate not in counts dict"

def register(user: str):
    """
    Register <user> to vote
    """
    r = json.loads(requests.post(f"{url}/register", data = {"id": user}).text)
    return r

def vote(user: str, target: str):
    """
    Cast a vote from <user> to <target>
    """
    r = json.loads(requests.post(f"{url}/addvote", data = {"id": user, "target": target}).text)
    return r

def getwhitelist():
    """
    Get whitelisted users
    """
    r = json.loads(requests.get(f"{url}/getwhitelist").text)
    return r

def getblacklist():
    """
    Get blacklisted users
    """
    r = json.loads(requests.get(f"{url}/getblacklist").text)
    return r

def blacklist(id: str):
    """
    Admin only: blacklist a user
    """
    r = json.loads(requests.post(f"{url}/blacklist", data = {"id": id}).text)
    return r

def whitelist(id: str):
    """
    Admin only: whitelist a user
    """
    r = json.loads(requests.post(f"{url}/whitelist", data = {"id": id}).text)
    return r

def getstatus():
    """
    Get the bot's current status
    """
    r = json.loads(requests.get(f"{url}/getstatus").text)
    return r

def changestatus(status: str):
    """
    Change the bot's current status
    """
    r = json.loads(requests.post(f"{url}/changestatus", data = {"status": status}).text)
    return r

def open():
    """
    Open voting
    """
    r = json.loads(requests.post(f"{url}/openclose", data = {"action": "open"}))
    return r

def close():
    """
    Close voting
    """
    r = json.loads(requests.post(f"{url}/openclose", data = {"action": "close"}))
    return r