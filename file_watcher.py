
import time
import os
import hashlib
import multiprocessing as mp

from wizard import Wizard
from uploader import Malware
from dbio import Database
#CLASS that pulls files from the unprocessed collection, processes them, and adds them to the processed collection
class FileGrab:
    #   is_running -boolean
    #   number_of_file_to_grab_each_iter -integer
    #   time_between_each_iter  -integer
    #   input_dir   -string
    #   output_dir  -string
    #   file_process_callback   -function
    #   proc    -multiprocessing.Process
    #   PARAM file_process_callback function that is invoked to perform processing
    def __init__(self, file_process_callback):
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


    #   stops the currently running instance of FileGrab and terminates its process
    def stop(self):
        if(self.is_running):

            print ""
            print "----BACKGROUND PROCESSING STOPPED----"
            print ""

            self.is_running = False
            self.proc.terminate()
    #   starts the FileGrab runnning and updates frequency information then starts self.proc
    #   PARAM wizard the wizard object that contains all the information for number of files and frequency if pulls
    def run(self, wizard):
        if(self.is_running == False):

            print ""
            print "----BACKGROUND PROCESSING RUNNING----"
            print ""

            if wizard.getTimeInterval() < 0 or wizard.getFileGrabInterval() < 0:
                self.number_of_file_to_grab_each_iter = 1
                self.time_between_each_iter = 10
            else:
                self.number_of_file_to_grab_each_iter = wizard.getFileGrabInterval()
                self.time_between_each_iter = wizard.getTimeInterval()


            self.is_running = True

            self.proc = mp.Process(target=self.run_loop)

            self.proc.daemon = True
            self.proc.start()
    #   function which is utilized by FileGrab to get files, move them, and perform processing
    def run_loop(self):

        try:
            while True:
                files = self.grab_files_names()
                filename_path_dict = self.move_files(files)
                malware_array = self.paths_to_malware_objs(filename_path_dict)

                self.process_files(malware_array)
                time.sleep(self.time_between_each_iter)
        # when self.stop() terminates the run loop
        except Exception as e:
            print(e)
    #   gets a list of the files in the unprocessed collection and shortens it to length = number_of_file_to_grab_each_iter
    #   RETURNS files_clipped a list of filenames of no greater than number_of_file_to_grab_each_iter
    def grab_files_names(self):
        only_files = [f for f in os.listdir(self.input_dir) if os.path.isfile(os.path.join(self.input_dir, f))]

        if len(only_files) > self.number_of_file_to_grab_each_iter:
            files_clipped = only_files[:self.number_of_file_to_grab_each_iter]
        else:
            files_clipped = only_files

        return files_clipped
    #   moves files from the unprocessed directory to the processed directory
    #   PARAM files a list of filenames of files to be moved
    #   RETURNS filename_path_dict a dictionary which maps filenames to their new paths
    def move_files(self,files):
        filename_path_dict = {}

        for file in files:
            os.rename("{0}/{1}".format(self.input_dir, file), ("{0}/{1}".format(self.output_dir, file)))
            full_path = os.path.join(self.output_dir, file)
            filename_path_dict[file] = full_path

        return filename_path_dict
    #   gets the new file paths of each file to be processed, generates hashes, adds it to the database and collects all the files in an array
    #   PARAM filename_path_dict a dictionary which maps filenames to their relative paths
    #   RETURNS malware_array a list of Malware objects to be processed
    def paths_to_malware_objs(self, filename_path_dict):

        malware_array = []

        for file in filename_path_dict:
            path = filename_path_dict[file]

            opened_file = open(path)
            read_file = opened_file.read()

            sha1= hashlib.sha1(read_file).hexdigest()
            sha256 = hashlib.sha256(read_file).hexdigest()
            md5 = hashlib.md5(read_file).hexdigest()
            hashes = {"sha1":sha1, "sha256":sha256, "md5":md5}

            malware = Malware(file, path, hashes)
            Database.db_insert_malware_obj(malware)
            malware_array.append(malware)

        return malware_array

    #   invokes the function specified in file_process_callback on a malware_array
    #   PARAM malware_array a list of Malware objects to be processed
    def process_files(self,malware_array):

        print ""
        print "----AUTO PROCESSING {0} FILES----".format(len(malware_array))
        print ""

        self.file_process_callback(malware_array)

if __name__ == '__main__':
    f = FileGrab(file_process_callback)
    f.run()
