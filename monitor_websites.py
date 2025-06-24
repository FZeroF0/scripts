import requests
import time
import os
import subprocess # For desktop notifications
import sys # For exiting if essential config is missing

# --- Configuration ---

# IMPORTANT: REPLACE THIS WITH YOUR Gist's RAW content URL.
# This is where your Flask/Ngrok script puts the latest Ngrok URL.
# How to get it:
# 1. Go to your Gist on GitHub.
# 2. Click on the file containing your Ngrok URL.
# 3. Click the "Raw" button.
# 4. Copy the URL from your browser's address bar.
GIST_RAW_URL = os.environ.get("GIST_RAW_URL")

# List of static URLs you always want to monitor
STATIC_URLS_TO_MONITOR = [
    "https://www.youtube.com",
    "https://coddy.tech",
    "https://this-website-is-fake-123xyz.com"
]

# How often to check websites (in seconds).
# 300 seconds = 5 minutes
CHECK_INTERVAL_SECONDS = 300

# --- Functions ---

def get_current_ngrok_url_from_gist(gist_raw_url):
    """
    Fetches the current Ngrok URL from the content of a GitHub Gist.
    Assumes the Gist content is just the Ngrok URL string.
    """
    if not gist_raw_url or gist_raw_url == "https://gist.githubusercontent.com/YOUR_USERNAME/YOUR_GIST_ID/raw/YOUR_FILENAME":
        print("[ERROR] GIST_RAW_URL is not configured. Cannot fetch Ngrok URL.")
        return None

    try:
        # Use a timeout to prevent the script from hanging indefinitely
        response = requests.get(gist_raw_url, timeout=10)
        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        
        ngrok_url = response.text.strip()
        print(f"[INFO] Successfully retrieved Ngrok URL from Gist: {ngrok_url}")
        return ngrok_url
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Could not retrieve Ngrok URL from Gist (Is the Gist URL correct? Is there internet?): {e}")
        return None

def check_website_status(url):
    """
    Checks if a given URL is accessible and returns its status.
    Returns (True, status_code) if up, (False, error_message) if down.
    """
    try:
        # Send a GET request with a timeout
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return True, response.status_code
        else:
            # For non-200 but successful responses (e.g., 404 Not Found, 302 Redirect)
            return False, f"HTTP Status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection Error (Cannot reach host)"
    except requests.exceptions.Timeout:
        return False, "Timeout (Request took too long)"
    except requests.exceptions.HTTPError as e:
        # This catches 4xx/5xx errors raised by response.raise_for_status()
        return False, f"HTTP Error: {e.response.status_code} {e.response.reason}"
    except requests.exceptions.RequestException as e:
        # Catch any other requests-related errors
        return False, f"Generic Request Error: {e}"

def send_desktop_notification(title, message):
    """
    Sends a desktop notification using dunstify.
    Make sure `dunst` is installed and running (`sudo pacman -S dunst`).
    """
    try:
        subprocess.run(['dunstify', '-a', 'WebsiteMonitor', title, message], check=True)
    except FileNotFoundError:
        print("[WARNING] 'dunstify' command not found. Install dunst (`sudo pacman -S dunst`) for desktop notifications.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to send dunstify notification: {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred while sending notification: {e}")

# --- Main Monitoring Loop ---

def main():
    print("Starting website monitoring...")
    
    # Check if dunstify is available at script start
    try:
        subprocess.run(['which', 'dunstify'], check=True, capture_output=True)
        dunstify_available = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        dunstify_available = False
        print("[WARNING] dunstify command not found. Desktop notifications will be disabled.")


    while True:
        # Create a list of URLs to check for this cycle
        urls_to_check = list(STATIC_URLS_TO_MONITOR)

        # Attempt to get the current Ngrok URL from the Gist
        ngrok_url = get_current_ngrok_url_from_gist(GIST_RAW_URL)
        if ngrok_url:
            urls_to_check.append(ngrok_url)
        else:
            print("[WARNING] Skipping Ngrok URL check this cycle due to retrieval failure. Ensure your Ngrok script is running and updating the Gist correctly.")

        print(f"\n--- Checking Websites ({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}) ---")
        
        if not urls_to_check:
            print("[INFO] No URLs to check. Please configure STATIC_URLS_TO_MONITOR or fix GIST_RAW_URL.")

        for url in urls_to_check:
            print(f"Checking: {url}...")
            is_up, status = check_website_status(url)
            
            if is_up:
                print(f"  [UP] {url} (Status: {status})")
            else:
                print(f"  [DOWN] {url} (Reason: {status})")
                if dunstify_available:
                    send_desktop_notification(
                        f"Website Down Alert!",
                        f"URL: {url}\nReason: {status}"
                    )

        print(f"--- Next check in {CHECK_INTERVAL_SECONDS} seconds ---")
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
