import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
# Replace with the Gist ID from the URL you copied (e.g., 'some_long_id_string' from gist.github.com/yourusername/some_long_id_string)
GIST_ID = os.environ.get("GIST_ID")
# Replace with the filename you chose in the Gist (e.g., 'current_website_url.txt')
GIST_FILENAME = os.environ.get("GIST_FILENAME")
# Replace with your GitHub Personal Access Token (PAT) - KEEP THIS SECURE!
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

# Ngrok's local API endpoint
NGROK_API_URL = "http://127.0.0.1:4040/api/tunnels"
GITHUB_GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_ngrok_url():
    """Fetches the current Ngrok public URL from the local API."""
    try:
        response = requests.get(NGROK_API_URL, timeout=5)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        # Find the HTTPS tunnel
        for tunnel in data.get("tunnels", []):
            if tunnel.get("proto") == "https":
                return tunnel.get("public_url")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Ngrok URL: {e}")
        return None

def update_github_gist(new_url):
    """Updates the content of the specified GitHub Gist."""
    if not new_url:
        print("No new Ngrok URL to update Gist with.")
        return False

    print(f"Attempting to update Gist with new URL: {new_url}")

    # Prepare the payload for the Gist update API
    payload = {
        "files": {
            GIST_FILENAME: {
                "content": new_url
            }
        }
    }

    try:
        response = requests.patch(GITHUB_GIST_API_URL, headers=HEADERS, data=json.dumps(payload), timeout=10)
        response.raise_for_status()
        print("GitHub Gist updated successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error updating GitHub Gist: {e}")
        print(f"Response content: {response.text if 'response' in locals() else 'N/A'}")
        return False

def main():
    last_known_url = None
    while True:
        current_ngrok_url = get_ngrok_url()

        if current_ngrok_url and current_ngrok_url != last_known_url:
            print(f"New Ngrok URL detected: {current_ngrok_url}")
            if update_github_gist(current_ngrok_url):
                last_known_url = current_ngrok_url
        elif not current_ngrok_url:
            print("Ngrok tunnel not detected or API unreachable. Retrying...")
        else:
            print(f"Ngrok URL is unchanged: {current_ngrok_url}. No update needed.")

        # Check every 5 minutes (300 seconds)
        time.sleep(300)

if __name__ == "__main__":
    # Install requests library if you haven't: pip install requests
    # If running as systemd service, make sure it has access to pip-installed packages
    print("Starting Ngrok URL updater script...")
    main()
