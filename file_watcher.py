
import time
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import multiprocessing as mp

#NOTE not pretty clean up
from uploader import Malware
#NOTE really there should be a better way to "upload"
#malware and add to database then FileGrab but ...

#TODO Make sure we are moving files at the last second or they could be in limbo

class FileGrab:
    def __init__(self, Database, file_process_callback):

        #NOTE not pretty clean up
        self.Database = Database

        self.is_running = False
        self.number_of_file_to_grab_each_iter = 1
        self.time_between_each_iter = 10 #seconds I think?

        current_dir_path = os.path.dirname(os.path.realpath(__file__))

        self.input_dir = os.path.join(current_dir_path, "background_files_unprocessed")
        if not os.path.exists(self.input_dir):
            os.makedirs(self.input_dir)

        self.output_dir = os.path.join(current_dir_path, "background_files_processed")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.file_process_callback = file_process_callback

        self.proc = mp.Process(target=self.run_loop)

    def set_files_per_sec(files_count, sec):
        self.number_of_file_to_grab_each_iter = files_count
        self.time_between_each_iter = sec #seconds I think?

    def set_files_per_sec(file_amount, sec):
        self.number_of_file_to_grab_each_iter = file_amount
        self.time_between_each_iter = sec #seconds I think?

    def stop(self):
        if(self.is_running):

            print ""
            print "----BACKGROUND PROCESSING STOPPED----"
            print ""

            self.is_running = False
            self.proc.terminate()

    def run(self):
        if(self.is_running == False):

            print ""
            print "----BACKGROUND PROCESSING RUNNING----"
            print ""


            self.is_running = True

            self.proc = mp.Process(target=self.run_loop)

            self.proc.daemon = True
            self.proc.start()

    def run_loop(self):

        try:
            while True:
                files = self.grab_files_names()
                filename_path_dict = self.move_files(files)
                malware_array = self.paths_to_malware_objs(filename_path_dict)

                #NOTE IDEALLY FILEWATCHER WOULD JUST WORK AND CATCH THE FILES BUT ...
                self.process_files(malware_array)

                time.sleep(self.time_between_each_iter)

        except Exception as e:
            print(e)
            # self.proc.terminate()


    def grab_files_names(self):
        only_files = [f for f in os.listdir(self.input_dir) if os.path.isfile(os.path.join(self.input_dir, f))]

        if len(only_files) > self.number_of_file_to_grab_each_iter:
            files_clipped = only_files[:self.number_of_file_to_grab_each_iter]
        else:
            files_clipped = only_files

        return files_clipped

    def move_files(self,files):

        #{"filename":"path/to/file", "filename":"path/to/file"}
        filename_path_dict = {}

        for file in files:
            os.rename("{0}/{1}".format(self.input_dir, file), ("{0}/{1}".format(self.output_dir, file)))
            full_path = os.path.join(self.output_dir, file)
            filename_path_dict[file] = full_path

        return filename_path_dict

    #NOTE not pretty clean up
    def paths_to_malware_objs(self, filename_path_dict):

        malware_array = []

        for file in filename_path_dict:

            path = filename_path_dict[file]
            malware = Malware(file, path)

            self.Database.db_insert_malware_obj(malware)

            malware_array.append(malware)

        return malware_array


    def process_files(self,malware_array):

        print ""
        print "----AUTO PROCESSING {0} FILES----".format(len(malware_array))
        print ""

        self.file_process_callback(malware_array)

class Watcher:

    def __init__(self):
        self.observer = Observer()
        self.event_handler = Handler()

    def run(self, cb):
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

def file_process_callback(files):
    for file in files:
        print "FILE ON THE OTHER END"
        print file


if __name__ == '__main__':
    f = FileGrab(file_process_callback)
    f.run()
