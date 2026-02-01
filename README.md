# Streamlit to Executable Template

This repository attempts to successfully create a low-code Streamlit executable (.exe) that automatically terminates its background process when the application is closed by the user.

A common issue when packaging Streamlit apps with PyInstaller is that closing the browser tab does not stop the Python server, leaving "zombie processes" consuming memory in the background. This template addresses this problem using a heartbeat mechanism.
If you have any ideas, improvements, or encounter issues, please open an issue in this repository.

## How it Works

The solution uses a client-server architecture to monitor activity.

1.  **The Launcher:** When you run the executable, it starts a local "Watchdog" server in the background and then launches your Streamlit application.
2.  **The Heartbeat:** A small JavaScript snippet injected into your Streamlit app sends periodic "pings" to the Watchdog to indicate that the page is open and active.
3.  **Auto-Shutdown:** If the user closes the browser tab, the pings stop. The Launcher detects this silence and, after a set timeout (default is 5 minutes), automatically kills the process.

**Note on Timeout:** The 5-minute delay is required because modern browsers (like Chrome) throttle JavaScript in inactive tabs to save battery. If the user minimizes the window, pings may slow down significantly. A longer timeout prevents the app from closing accidentally while running in the background.

## Performance and Known Issues
File Size: The resulting .exe will be approximately 80MB.
Startup Time: It may take a few seconds for the browser to open after double-clicking the executable. It is important not to click multiple times during this loading phase.

## Usage

### 1. Prepare your App
Copy and paste the required JavaScript snippet into your `app.py` file. This is necessary to send the signals to the launcher.

### 2. Build the Executable
Use `launcher.py` as the entry point for PyInstaller. I have tested this on Windows.

To create a single-file executable without a console window, run the following command in your terminal:

```bash
pyinstaller --noconfirm --onefile --windowed --name "MyApp" --copy-metadata streamlit --collect-all streamlit --add-data "app.py;." launcher.py ```
