import time
from watchdog.observers import Observer
from detector.watcher.ChangeHandler import ChangeHandler


class FileWatcher:

    def __init__(self, watch_directory='.'):
        self.observer = Observer()
        self.watch_directory = watch_directory

    def run(self):
        print("Watching directory \"" + self.watch_directory + "\" for changes")
        event_handler = ChangeHandler()
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(30)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()
