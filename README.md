# My Utility Scripts

A collection of useful scripts for development, system administration, and automation. This repository serves as a personal toolkit to streamline various tasks related to local development, system monitoring, and DevOps practices.

## Table of Contents

* [Scripts Included](#scripts-included)
    * [Ngrok URL Auto-Updater](#ngrok-url-auto-updater)
    * [System Resource Monitor](#system-resource-monitor)
* [Getting Started](#getting-started)
* [Contributing](#contributing)
* [License](#license)

## Scripts Included

### Ngrok URL Auto-Updater

* **Description:** This Python script automates the process of fetching the active ngrok public URL and updating an external service or a local configuration file with this URL. It's particularly useful for testing webhooks or integrating local applications with external services during development without manual URL updates.
* **Technologies:** Python, `requests` library (for HTTP requests), `pyngrok` (for interacting with ngrok API).
* **How to Use:**
    1.  **Prerequisites:** Ensure `ngrok` is installed and running on your system, and you have an ngrok authtoken configured.
    2.  **Install Python dependencies:**
        ```bash
        pip install requests pyngrok
        ```
    3.  **Configure:** Modify the script (e.g., `ngrok_updater.py`) to specify the target API endpoint, file path, or other destination where the ngrok URL needs to be updated. You might need to add API keys or tokens as environment variables.
    4.  **Run:** Execute the script after starting your ngrok tunnel.
        ```bash
