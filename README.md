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
    3.  **Configure:** Modify the script to specify the target API endpoint, file path, or other destination where the ngrok URL needs to be updated. You might need to add API keys or tokens as environment variables.
    4.  **Run:** Execute the script after starting your ngrok tunnel.
        ```bash
        python update_ngrok_url.py
        ```

### System Resource Monitor

* **Description:** A Python script designed to monitor key system resources such as CPU usage, memory consumption, and disk space. It can log this information, display it in the terminal, or send alerts if certain thresholds are exceeded. This is valuable for understanding system performance and identifying potential bottlenecks.
* **Technologies:** Python, `psutil` library (for system monitoring).
* **How to Use:**
    1.  **Prerequisites:** Python 3.x.
    2.  **Install Python dependencies:**
        ```bash
        pip install psutil
        ```
    3.  **Configure:** Adjust monitoring intervals, thresholds, and output/alerting methods within the script.
    4.  **Run:** Execute the script. It can be run as a background process or a scheduled task.
        ```bash
        python monitor_websites.py
        ```

## Getting Started

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/FZeroF0/scripts.git](https://github.com/FZeroF0/scripts.git)
    cd scripts
    ```
2.  **Install script-specific dependencies:**
    Each script's "How to Use" section specifies its required Python libraries. Install them using `pip`.
3.  **Run the scripts:**
    Refer to the "How to Use" section for each script.

## Contributing

Feel free to fork this repository and add your own useful scripts! When contributing, please:

* Provide a clear description of the script's purpose.
* Detail its prerequisites and usage instructions.
* Ensure the script is well-commented and easy to understand.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
