import sys
from pathlib import Path
import logging
import os
from urllib.parse import unquote


def get_log_path():
    # https://stackoverflow.com/questions/43784468/pyinstaller-exe-file-doesnt-create-log-file
    if hasattr(sys, "_MEIPASS"):
        # Running as .exe, put logs in AppData
        log_dir = Path(os.getenv('APPDATA')) / "DeleteSSApp" / "logs"
    else:
        # Running as script, put logs next to script
        log_dir = Path(__file__).parent / "logs"

    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "delete_log.txt"

log_file = get_log_path()

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_delete(file_path):
    path = Path(file_path)

    if not path.exists():
        msg = f"Error: File does not exist: {path}"
        logging.error(msg)
        return msg
    if not path.is_file():
        msg = f"Error: Not a file: {path}"
        logging.error(msg)
        return msg
    name = path.name.lower()
    if "screenshot" not in name or not name.endswith(".png"):
        msg = f"Skipped: Not a valid screenshot PNG: {path.name}"
        logging.info(msg)
        return msg
    try:
        path.unlink()
        msg = f"Deleted: {path}"
        logging.info(msg)
        return msg
    except Exception as e:
        msg = f"Failed to delete {path}: {e}"
        logging.error(msg)
        return msg

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("No file path provided")
        sys.exit(1)

    file_arg = sys.argv[1]

    prefix = "deleteSS://"
    if file_arg.lower().startswith(prefix.lower()):
        file_path = unquote(file_arg[len(prefix):])
    else:
        file_path = file_arg

    file_path = file_path.replace('/', '\\')
    
    result = safe_delete(file_path)
    print(result)
    sys.exit(0)
