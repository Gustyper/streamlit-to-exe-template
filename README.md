# Streamlit to Executable Template

This repository successfully creates a low-code Streamlit executable (.exe) that automatically terminates its background process when the application is closed by the user.

A common issue when packaging Streamlit apps with PyInstaller is that closing the browser tab does not stop the Python server, which keeps consuming memory in the background. This template addresses this problem using a JavaScript activity control mechanism.

If you have any ideas, improvements, or encounter issues, please open an issue in this repository.

## How it Works

The solution uses a client-server architecture to monitor activity.

1.  **The Launcher:** When you run the executable, it starts a local server in the background whose only purpose is to track Streamlit activity. After that, it launches the Streamlit application.
2.  **The Heartbeat:** A small JavaScript snippet injected into your Streamlit app sends periodic "pings" to indicate that the page is open and active.
3.  **Auto-Shutdown:** If the user closes the browser tab, the pings stop. The Launcher detects this silence and, after a set timeout (default is 5 minutes), automatically kills the process.

**Note on Timeout:** The 5-minute delay is required because some modern browsers may track tab activity and stop Javascript processes to save battery. If the user minimizes the window, pings may slow down significantly. A longer timeout prevents the app from closing accidentally while running in the background.

## Usage

### 1. Prepare your App
Copy and paste the required JavaScript snippet into your `app.py` file. This is necessary to send the signals to the launcher.

### 2. Build the Executable
Use `launcher.py` as the entry point for PyInstaller. I have tested this on Windows.

In order to create the executable, you have to create a Python virtual environment to avoid loading unused dependencies and getting files that are too big to share.

1.  Create a Python environment: `python -m venv venv`
2.  Activate the environment: `venv\Scripts\activate`
3.  Install your project dependencies: `pip install -r requirements.txt`
4.  Run the PyInstaller command.

**Recommended Command (Faster Startup):**
```bash
pyinstaller --noconfirm --onedir --windowed --name "MyApp" --copy-metadata streamlit --collect-all streamlit --add-data "app.py;." launcher.py
```

## Understanding the Tags (Flags)

- `--noconfirm`: Does not ask for confirmation to overwrite the output folder if it already exists.

- `--onedir`: Creates a folder containing the executable and all dependencies unpacked. This is faster to load. (Alternative: `--onefile` creates a single `.exe`, but it is slower).

- `--windowed`: Hides the terminal/console window when the app runs.

- `--name "MyApp"`: Sets the name of your executable file.

- `--copy-metadata streamlit`: Copies configuration data required by the Streamlit package.

- `--collect-all streamlit`: Forces PyInstaller to collect all internal dependencies of Streamlit.

- `--add-data "app.py;."`: Adds your script file to the bundle.  
  **Note:** On Windows use `;`, on Linux/Mac use `:`.

---

## Performance and Final .exe Results

Regarding the `.exe` output options, you can choose between a single `.exe` file (`--onefile`) or a folder with preloaded libraries (`--onedir`). The second option loads way faster after clicking on the file inside the folder, and it is the recommended one.

### File Size

The resulting single file `.exe` with only the default template libraries will be approximately 80MB. If you use the folder method (recommended), you will end up with a ~30MB `.zip` file that can be shared more easily. The shortcoming is the need to share the whole folder, whereas a single file is more straightforward for most users.

### Startup Time

If you use a single file (`--onefile`), you can expect the application to open about 1 minute after clicking, which may be a bit tiresome. With the folder method (`--onedir`), it takes only a few seconds.