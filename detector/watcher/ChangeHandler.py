import time
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    file_cache = {}

    def on_any_event(self, event):
        if event.is_directory:
            return None

        seconds = int(time.time())
        key = (seconds, event.src_path)
        if key in self.file_cache:
            return
        self.file_cache[key] = True

        if event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            print("Watchdog received modified event - % s." % event.src_path)
        elif event.event_type == 'deleted':
            print("Watchdog received deleted event - % s." % event.src_path)
