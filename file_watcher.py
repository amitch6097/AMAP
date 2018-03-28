
import time
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:

    def __init__(self):
        self.observer = Observer()
        self.event_handler = Handler()

    def print_s(self):
        print "SSSSS"

    def run(self):
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        downloads_dir = os.path.join(current_dir_path, "downloads")

        self.observer.schedule(self.event_handler, downloads_dir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Error"

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print "Received created event - %s." % event.src_path

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print "Received modified event - %s." % event.src_path


# if __name__ == '__main__':
#     w = Watcher()
#     w.run()
