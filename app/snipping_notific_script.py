from winotify import Notification, audio
from pathlib import Path
import config

def notify(path):
    print(f"Notify called for: {path}")
    toast = Notification(app_id="Snipping Notification Script",
                        title="Screenshot copied to clipboard", 
                        msg="Automatically saved to screenshots folder.",
                        duration="long",
                        icon=f"{path}",
                        )

    toast.set_audio(audio.SMS, loop=False)
    toast.add_actions(label="Delete", launch=f"deleteSS://{path}")
    toast.add_actions(label="Edit", launch=f"{path}") #Launches file for now..

    toast.show()

if __name__ == "__main__":
    import time
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class ScreenshotHandler(FileSystemEventHandler):
        def on_created(self, event):
            print(f"File created: {event.src_path}")
            if not event.is_directory:
                notify(event.src_path)
            return super().on_created(event)
        
    path =  config.SS_Path
    print(f"Watching path: {path}")

    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=False)
    observer.start()


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()