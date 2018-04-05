import multiprocessing as mp
from multiprocessing import Process, Queue

import os
import subprocess
import sys
from time import gmtime, strftime
import time
from datetime import datetime
import dbio
import gevent
from gevent import monkey; monkey.patch_all()
from dbio import Database

from cuckoo_module import CuckooModule
Cuckoo = CuckooModule()


#CLASS to handle one file with X many modules running on it
class Process:
    def __init__(self, file_id, file_name):
        self.file_id =  file_id
        self.file_name = file_name

        #modules is a dictionary w/
        # {'module name': wether or not module passed/ran}
        # Ex {'ratDecoder':False} -> ratDecoder failed to run on file
        self.modules = {}

        self.percent_done = 0
        self.start_time = "idle"
        self.end_time = "waiting..."
        self.run_number = -1
        self.id = -1
        self.modules_ignore = ["cuckoo_id", "Cuckoo"]
        self.starttime_num = 0
        self.endtime_num = 0


    def edit_id(self, id):
        self.id = id

    def add_module(self, module):
        self.modules[module] = False

    def print_modules(self):
        for key in self.modules:
            print "KEY:{0} VALUE:{1}".format(key, self.modules[key])

    #sets the process to finished and puts a timestamp on it
    def finish_process(self):
        self.percent_done = 100
        self.end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.endtime_num = time.time()

    #gives start timestamp
    def start_process(self):
        self.start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.starttime_num = time.time()
        self.end_time = "running..."

    #Get the number of runs the file has been through
    #
    #   Database  - our global database object
    def get_file_runs(self):
        # assert self.file_id != -1
        self.run_number = Database.db_inc_runs_by_id(self.file_id)

    #for putting the process into the database
    def to_database_file(self):
        length = self.endtime_num - self.starttime_num
        Database.db_add_avgtime(length)
        return {'file_id':self.file_id,
            "file_name":self.file_name,
             "modules":self.modules,
             "run_number":self.run_number,
             "start_time":self.start_time,
             "end_time":self.end_time
        }

    def from_database_file(self, db_file):
        self.id = db_file["_id"]
        self.modules = db_file["modules"]
        self.run_number = db_file["run_number"]
        self.start_time = db_file["start_time"]
        self.end_time = db_file["end_time"]

    #processes the string data output of a processes
    def processData(self, data):
        retList = []
        aStr = ""
        print(data)
        if "Unabel to match" not in data and "Importing Decoder" in data:
            Database.db_add_malware(time.time())
        for c in data:
            if c == "\n":
                retList.append(aStr)
                aStr = ""
            else:
                aStr += c
        return retList

    def check_cuckoo(self, file_path):
        if "Cuckoo" in self.modules.keys():
            response_id = Cuckoo.submit_file( file_path)
            if response_id == None:
                return {}

            output_obj = {'cuckoo_id':response_id, "Cuckoo":""}

            Database.db_update_malware_on_id(self.file_id, output_obj)
            return output_obj
        else:
            return {}

    def run(self):
        self.start_process()
        cwd = os.getcwd()

        db_file_obj = Database.db_find_by_id(self.file_id)
        Database.db_gui_insert_newtype(db_file_obj['Name'].split(".")[-1])
        output_obj = self.check_cuckoo(db_file_obj['location'])

        for module in self.modules:
            if module in self.modules_ignore:
                continue

            #location main python file in modules folder on system
            location_of_module = '{0}/modules/{1}/{1}.py'.format(cwd, module)

            p = subprocess.Popen(['python', location_of_module, db_file_obj['location']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdoutdata, stderrdata = p.communicate()

            #if we get error data the module 'failed'
            module_passed = True
            if stderrdata:
                module_passed = False
            self.modules[module] = module_passed

            output = self.processData(stdoutdata)
            output_obj[module] = output

        self.finish_process()
        Database.db_update_malware_on_id(db_file_obj["_id"], output_obj)
        Database.db_update_process(self.id, self.to_database_file())




class MultiProcessor:
    def __init__(self):
        self.cpu_count = mp.cpu_count()
        self.processes = []
        self.queue = Queue()

    def start(self):
        self.processes = [mp.Process(target=self.run, args=(self.queue,)) for i in range(self.cpu_count)]
        for proc in self.processes:
            proc.start()

    def add_to_queue(self, process):
        self.queue.put(process)

    def pop_queue(self):
        return self.queue.get()

    def join_all():
        for proc in self.processes:
            proc.join()

    def run(self, q):
        while(True):
            process = q.get()
            process.run()


#CLASS to create process objects and run them
class Processor:
    def __init__(self, Wizard):
        self.Wizard = Wizard
        self.modules = []       #all prossible modules we can run
        self.new_processes = [] #processes that need to be run still
        self.old_processes = [] #processes that have been run
        self.Multiproc = MultiProcessor()
        self.Multiproc.start()
        self.is_running = False
        self.non_editable_modules = ["Cuckoo"]


    # for displaying all of the processes, already run or running
    def get_all_processes(self):
        return self.old_processes + self.new_processes

    def get_all_processes_db(self):
        process_stack = Database.db_get_all_processes()
        processes = self.process_stack_to_processes(process_stack)
        return processes

    def process_stack_to_processes(self, db_process_stack):
        processes = []
        for db_process in db_process_stack:

            file_id = db_process['file_id'];
            file = Database.db_find_by_id(file_id)

            process = Process(file['_id'], file['Name'])
            process.from_database_file(db_process)
            processes.append(process)

        return processes

    def get_editable_modules(self):
        modules = self.get_modules()
        for to_remove in self.non_editable_modules:
            if to_remove in modules:
                modules.remove(to_remove)
        return modules

    #get all of the possible modules we can run
    def get_modules(self):
        self.modules = []

        # open the modules dir and make an array of all folders in there
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        modules_folder = "{0}/modules".format(current_dir_path)

        for file_or_dir in os.listdir(modules_folder):
            if os.path.isdir("{0}/{1}".format(modules_folder, file_or_dir)):
                self.modules.append(file_or_dir)

        #for some reason this folder shows up when unzipping on mac so delete it
        self.modules = [x for x in self.modules if x != "__MACOSX"]

        if(Cuckoo.is_available()):
            self.modules.append("Cuckoo")

        return self.modules

    #creates a process object from a form and uploads
    #
    #   forms                  - a form submitted through a post action
    #   uploaded_malware_array - array of Malware Objects see Uploader.py
    #   Database               - our global database object
    def create_process_obj(self, forms, uploaded_malware_array):

        #loop through malware objects
        for current_file in uploaded_malware_array:
            #create a process object from it
            process = Process(current_file.id, current_file.filename)
            # get the nummber of times the file has been run
            process.get_file_runs()

            # loop through all of the possible modules
            for index, module in enumerate(self.modules):

                # the name of the check box input is the form
                # 'FILENAME_INDEX-OF-MODULE'
                name = "{0}_{1}".format(current_file.filename, index)

                #grab the checkbox value
                checkbox = forms.get(name)

                #if it is on
                if (checkbox == 'on'):
                    #add the string name to the process's modules
                    process.add_module(module)

            #insert the process into the database
            Database.db_proc_insert(process)

            #add the process to list of processes that still need to be processed
            self.new_processes.append(process)


    def create_process_obj_auto(self, files_array):
        for file in files_array:
            modules_array = self.Wizard.getModules()
            auto_modules_config = { x : True for x in modules_array }

            process = Process(file.id, file.filename)
            process.get_file_runs()

            for module in auto_modules_config:
                if(auto_modules_config[module] == True):
                    process.add_module(module)

            #insert the process into the database
            Database.db_proc_insert(process)
            #add the process to list of processes that still need to be processed
            self.new_processes.append(process)
        self.run_modules()

    def get_cuckoo(self, file_database_obj):
	print file_database_obj.keys()
        if 'Cuckoo' in file_database_obj.keys():
            if file_database_obj['Cuckoo'] == "":
                task_id = file_database_obj['cuckoo_id']
		print task_id
                response = Cuckoo.get_report(task_id)
		print response
		if response != "":
                	Database.db_update_malware_on_id(file_database_obj['_id'], {"Cuckoo", response})
                return response
            return file_database_obj['Cuckoo']
        return None

    def run_modules(self):
        while self.new_processes:
            process = self.new_processes.pop()
            self.Multiproc.add_to_queue(process)
