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


"""
Describes the processing of a malware sample by multiple modules
int:    file_id, unique id given to a file when it is uploaded to the mongodb
string: file_name, filename of the file being processed
"""
class Process:
    #   PARAM file_id the unique id of the file
    #   PARAM file_name the name of the file
    #   file_id -integer
    #   file_name   -string
    #start_time -string to display in processes
    #end_time -string to display in processes
    #id -integer to display in processes
    #modules_ignore -list of module names this system will not use
    #starttime_num -integer representation of starttime
    #endtime_num -integer representaiton of endtime
    def __init__(self, file_id, file_name):
        self.file_id =  file_id
        self.file_name = file_name

        #modules is a dictionary w/
        # {'module name': wether or not module passed/ran}
        # Ex {'ratDecoder':False} -> ratDecoder failed to run on file
        self.modules = {}


        self.start_time = "idle"
        self.end_time = "waiting..."
        self.run_number = -1
        self.id = -1
        self.modules_ignore = ["cuckoo_id", "Cuckoo"]
        self.starttime_num = 0
        self.endtime_num = 0

    # PARAM id integer id that will be set
    def edit_id(self, id):
        self.id = id
    # PARAM module the module to be added to the process
    def add_module(self, module):
        """adds a module to the list of modules that will process the file"""
        self.modules[module] = False
    # print each module for this process and whether it is enabled
    def print_modules(self):
        """prints all of the modules which will process the file"""
        for key in self.modules:
            print "KEY:{0} VALUE:{1}".format(key, self.modules[key])

    def finish_process(self):
        """puts a timestamp on the process when finished"""
        self.percent_done = 100
        self.end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.endtime_num = time.time()

    def start_process(self):
        """puts a timestamp on the process when started"""
        self.start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.starttime_num = time.time()
        self.end_time = "running..."

    def get_file_runs(self):
        """upadates the number of runs the file has been through"""
        self.run_number = Database.db_inc_runs_by_id(self.file_id)

    def to_database_file(self):
        """returns a dictionary which can be used to place object into a mongodb"""
        length = self.endtime_num - self.starttime_num
        Database.db_add_avgtime(length)
        return {'file_id':self.file_id,
            "file_name":self.file_name,
             "modules":self.modules,
             "run_number":self.run_number,
             "start_time":self.start_time,
             "end_time":self.end_time
        }
    def to_database_file_html(self):
        """returns a dictionary which can be used to place object into html"""
        length = self.endtime_num - self.starttime_num
        Database.db_add_avgtime(length)
        return {'file_id':str(self.file_id),
            "file_name":self.file_name,
             "modules":self.modules,
             "run_number":self.run_number,
             "start_time":self.start_time,
             "end_time":self.end_time
        }

    def to_database_file_id(self):
        """returns a dictionary which has the file id"""
        if(self.id == -1):
            return
        return {'file_id':self.file_id,
            "file_name":self.file_name,
             "modules":self.modules,
             "run_number":self.run_number,
             "start_time":self.start_time,
             "end_time":self.end_time,
             "_id": self.id
        }
    #retrieve information from the database to be displayed
    # PARAM db_file the database file which contains the information
    def from_database_file(self, db_file):
        """can upadte a process object from mongodb information"""
        self.id = db_file["_id"]
        self.modules = db_file["modules"]
        self.run_number = db_file["run_number"]
        self.start_time = db_file["start_time"]
        self.end_time = db_file["end_time"]

    def processData(self, data):
        """processses output data from a module for displaying"""
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
    #submits a file to cuckoo then gets the id of the report
    #   PARAM file_path the path of the file being submitted
    #   RETURNS a dictionary containing the report id generated by cuckoo or an empty dicitonary
    def check_cuckoo(self, file_path):
        """checks if Cuckoo is avaiable and runs if possible"""

        if "Cuckoo" in self.modules.keys():
            response_id = Cuckoo.submit_file( file_path)
            if response_id == None:
                return {}

            output_obj = {'cuckoo_id':response_id, "Cuckoo":""}

            Database.db_update_malware_on_id(self.file_id, output_obj)
            return output_obj
        else:
            return {}
    #retrives a cuckoo report if cuckoo is installed and the report exists
    #   PARAM output_obj a dictionary with the cuckoo report id
    #   RETURNS output_obj the same parameter dictionary with the addition of the report pathname
    def get_cuckoo(self, output_obj):
        """retrives a cuckoo report if it is an avaiable module"""

        if "Cuckoo" in self.modules.keys():
            if "cuckoo_id" in output_obj.keys():
                response = ""
                while response == "":
                    response = Cuckoo.get_report(output_obj["cuckoo_id"])
                output_obj["Cuckoo"] = response
                return output_obj

        return output_obj

    #runs each of the modules a process has activated and updates th database
    def run(self):
        """runs all of the modules in a process on the given file and upates the mongodb"""

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
            module_dir = '{0}/modules/{1}/'.format(cwd, module)

            os.chdir(module_dir)
            p = subprocess.Popen(['python', "{0}.py".format(module), db_file_obj['location']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.chdir(cwd)
            stdoutdata, stderrdata = p.communicate()

            #if we get error data the module 'failed'
            module_passed = True
            if stderrdata:
                module_passed = False
            self.modules[module] = module_passed

            output = self.processData(stdoutdata)
            output_obj[module] = output

        Database.db_update_malware_on_id(db_file_obj["_id"], output_obj)
        Database.db_update_process(self.id, self.to_database_file())

        output_obj = self.check_cuckoo(output_obj)

        self.finish_process()
        Database.db_update_malware_on_id(db_file_obj["_id"], output_obj)
        Database.db_update_process(self.id, self.to_database_file())



"""Handles the multiporcessing of processes in the system"""
class MultiProcessor:
    # cpu_count -integer count of the systems cpus
    # processes -list list of processes this MultiProcessor is associated with
    # queue -Queue with manages the processes
    def __init__(self):
        self.cpu_count = mp.cpu_count()
        self.processes = []
        self.queue = Queue()

    # starts the multiprocessing
    def start(self):
        """starts the multiprocessing of current processes in the object"""
        self.processes = [mp.Process(target=self.run, args=(self.queue,)) for i in range(self.cpu_count)]
        for proc in self.processes:
            proc.start()
    # adds a new process to the queu
    #   PARAM process Process to be added to the queue
    def add_to_queue(self, process):
        self.queue.put(process)
    # RETURNS the queue's head
    def pop_queue(self):
        return self.queue.get()
    # joins all the processes so the program must wait for them
    def join_all():
        for proc in self.processes:
            proc.join()
    # runs each process
    def run(self, q):
        while(True):
            process = q.get()
            process.run()


"""Object to handle creating processes as well as starting the processing of processes"""
class Processor:
    def __init__(self, Wizard):
        self.Wizard = Wizard
        self.modules = []       #all prossible modules we can run
        self.new_processes = [] #processes that need to be run still
        self.old_processes = []
        # self.get_all_processes_db_old() #processes that have been run
        self.Multiproc = MultiProcessor()
        self.Multiproc.start()
        self.is_running = False
        self.non_editable_modules = ["Cuckoo"]


    """Displays all process in the current session"""
    def get_all_processes(self):
        return self.get_all_processes_db()

    """Displays all processes in old sessions"""
    def get_all_processes_db_old(self):
        process_stack = Database.db_get_all_processes_old()
        processes = self.process_stack_to_processes(process_stack)
        return processes

    """Displays all process in the current session"""
    def get_all_processes_db(self):
        process_stack = Database.db_get_all_processes()
        processes = self.process_stack_to_processes(process_stack)
        return processes

    """Creates processes from a list of mongodb processes"""
    def process_stack_to_processes(self, db_process_stack):
        processes = []
        for db_process in db_process_stack:

            file_id = db_process['file_id'];
            file = Database.db_find_by_id(file_id)

            process = Process(file['_id'], file['Name'])
            process.from_database_file(db_process)
            processes.append(process)

        return processes

    """Gets the current modules which can be edited"""
    def get_editable_modules(self):
        modules = self.get_modules()
        for to_remove in self.non_editable_modules:
            if to_remove in modules:
                modules.remove(to_remove)
        return modules

    """Gets all of the avaiable modules in the system editable and not"""
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

    """Creates a process from a html form and uploads list
    froms:              Bottle HTML form object
    uploads_name_array: list of malware objects
    """
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

    """Creates a batch of processes using the Wizard object config"""
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

    """Checks if cuckoo is a modules and tries to retrive a cuckoo report"""
    def get_cuckoo(self, file_database_obj):
    	print file_database_obj.keys()
        if 'Cuckoo' in file_database_obj.keys():
            if file_database_obj['Cuckoo'] == "":
                task_id = file_database_obj['cuckoo_id']
		print task_id
                response = Cuckoo.get_report(task_id)
		print response
		if response != "":
                	Database.db_update_malware_on_id(file_database_obj['_id'], {"Cuckoo": response})
                return response
            return file_database_obj['Cuckoo']
        return None

    """Triggers the start of the parrellel processing of process objects through MultiProcessor"""
    def run_modules(self):
        while self.new_processes:
            process = self.new_processes.pop()
            self.Multiproc.add_to_queue(process)
