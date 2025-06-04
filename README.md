# Snippet Notifications w/ Delete (Work in Progress)

This windows app creates a custom notifications with an "Delete" button, helping you keep your screenshots folder clean. The tool builds on the Snipping Tool which already takes a screenshot and copies the images to the clipboard.

![Image depicting the notification a recent screenshot with a delete button.](/Example_Notification.png)

## Installation

1.  **virtual environment (recommended) + Initial Setup:**
    * Create venv: `python -m venv venv`
    * Activate it: `source venv/Scripts/activate`
    * Install dependencies: `pip install -r requirements.txt` 

4.  **Declare your screenshot path `config.py`:**
    *   Create `/app/config.py` and add your screenshots folder path:
        - Format: `SS_Path=C:/Users/YourUsername/Pictures/Screenshots`

5.  **Executable & Registering Custom URL Protocol (`deleteSS://`):**
    *   Create an executable for the `delete_ss.py` script which does the actual deletion:
        - Run `pyinstaller --onefile --noconsole app/delete_ss.py`. This will create delete_ss.exe in a dist folder. The other newly created files can be deleted. 
        - **IMPORTANT:** Place the delete_ss.exe in a stable location, as the registry key will point to it. Preferably, place it in the `C:\\Program Files\...\delete_ss.exe`.
    *   To create the protocol, create a `.reg` with the following contents, replacing "EXACTPATH" with the path of your delete_ss.exe:
        ```reg
        Windows Registry Editor Version 5.00

        [HKEY_CURRENT_USER\Software\Classes\deleteSS]
        @="URL:DeleteSS Protocol"
        "URL Protocol"=""

        [HKEY_CURRENT_USER\Software\Classes\deleteSS\shell]

        [HKEY_CURRENT_USER\Software\Classes\deleteSS\shell\open]

        [HKEY_CURRENT_USER\Software\Classes\deleteSS\shell\open\command]
        @="\"C:\\Users\\...EXACTPATH...\\delete_ss.exe\" \"%1\"" 
        ```

## Usage

1.  **Create an executable for the notification script:**
    * The `snipping_notific_script.py` script watches the folder and shows notifications:
        - `pyinstaller --onefile --noconsole --name "Snipping Notific Script" app/snipping_notific_script.py` (ensure app/config.py is setup)

2.  **Running & Automation:**
    * Now open the new executable and it should run in the background. To view it open task manager or take a SS.
    * Automate on startup:
        - Press Windows + R, search `shell:startup`, place the "Snipping Notific Script.exe" into this folder
    * **TIP:** To avoid duplicate notifications, disable the default Windows Snipping Tool notifications:
        - Windows Settings > System > Notifications, find "Snipping Tool", and turn it off.
        - `Note:` This will diable all notifications including video clips or other Snipping Tool notifications* 


## Planned / Under Work: 
- Working Edit Button
    - Potentially through launching MS paint with the image
    - winotify doesn't support launching apps with args => potentially migrate to winrt
- A way to only disable snipping tool SS captures and not videos
- More extensive error logging & telling the user errors