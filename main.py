import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from discord_webhook import DiscordWebhook

def run_dummy_server():
    """Start a dummy HTTP server to bind to a port."""
    port = int(os.environ.get("PORT", 5000))  # Use the port Render assigns or default to 5000
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    print(f"Dummy server running on port {port}")
    server.serve_forever()

# Start the dummy server in a separate thread
threading.Thread(target=run_dummy_server, daemon=True).start()

# Webhook URL (replace with your actual webhook URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1330720300307845170/f2Xm40QZH2CNbI4hbL0FRr66hJjmU92DXbyDcp0Z970RbPL9H4Nd5WzY06xiF8nPGGMp"

def send_to_discord(message):
    """Send a message to Discord via the webhook."""
    try:
        webhook = DiscordWebhook(url=WEBHOOK_URL, content=message)
        response = webhook.execute()
        if response.status_code == 200:
            print("Message sent to Discord.")
        else:
            print(f"Failed to send message to Discord. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending webhook: {e}")

def main():
    """Main script logic."""
    print("Starting the process...")
    try:
        # Simulated user info (replace with actual data collection if applicable)
        user_info = {
            "username": os.getenv("USER", "Unknown User"),
            "platform": os.getenv("PLATFORM", "Linux"),
        }
        print(f"User information retrieved successfully: {user_info}")

        # Send user info to Discord webhook
        send_to_discord(f"User Info: {user_info}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    
