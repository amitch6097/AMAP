import multiprocessing as mp
from multiprocessing import Process, Queue

import os
import subprocess
import sys
from time import gmtime, strftime

import gevent
from gevent import monkey; monkey.patch_all()

#NOTE gevent queue doesnt work async with processes
#NOTE also mp.manager.queue doesn't work
# from gevent.queue import Queue

#OLD MULTIPROCESSING STUFF
#
# def add_processes(key, values):
#     return values
#
# def add_batch(batch_obj):
#     pool = mp.Pool(processes=4)
#     results = [pool.apply_async(add_processes, args=(key, batch_obj[key])) for key in batch_obj]
#     output = [p.get() for p in results]
#     print(output)
#
#
# if __name__ == '__main__':
#     dic = {'key':[1, 2, 3], 'key2':[1, 2 ,3]}
#     add_batch(dic)


#CLASS to handle one file with X many modules running on it
class Process:

    #
    #   file   - a Malware Object see Uploader.py
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
        self.modules_ignore = ["Cuckoo"]

    def edit_id(self, id):
        self.id = id

    #add a modules to dictionary see above
    #
    #   module    - name of module adding (string)
    def add_module(self, module):
        #all modules start as failing
        self.modules[module] = False

    #helps for debugging
    def print_modules(self):
        for key in self.modules:
            print "KEY:{0} VALUE:{1}".format(key, self.modules[key])

    #sets the process to finished and puts a timestamp on it
    def finish_process(self):
        self.percent_done = 100
        self.end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    #gives start timestamp
    def start_process(self):
        self.start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.end_time = "running..."

    #Get the number of runs the file has been through
    #
    #   Database  - our global database object
    def get_file_runs(self, Database):
        # assert self.file_id != -1
        self.run_number = Database.db_inc_runs_by_id(self.file_id)

    #for putting the process into the database
    def to_database_file(self):
        return {'file_id':self.file_id,
            "file_name":self.file_name,
             "modules":self.modules,
             "run_number":self.run_number,
             "start_time":self.start_time,
             "end_time":self.end_time,
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
        # print data
        for c in data:

            if c == "\n":
                retList.append(aStr)
                # print aStr
                aStr = ""
            else:
                aStr += c

        return retList

    def check_cuckoo(self, Database):
        #NOTE remove cuckoo because it is not run the same
        if "Cuckoo" in self.modules.keys() :
            #     print "---DOING CUCKOO THINGS---"
            #     # response_id = CUCKOOAPI.add_file()?
            response_id = 1

            output_obj = {'Cuckoo':response_id}
            Database.db_update_malware_on_id(self.file_id, output_obj)


    def run(self, Database):
        self.start_process()
        cwd = os.getcwd()

        # grab the file out of the databse because
        #we are updating the information on the file
        # output_obj = process.file.to_database_file()
        db_file_obj = Database.db_find_by_id(self.file_id)
        output_obj = {}

        self.check_cuckoo(Database)


        for module in self.modules:

            if module in self.modules_ignore:
                continue

            #location main python file in modules folder on system
            location_of_module = '{0}/modules/{1}/{1}.py'.format(cwd, module)

            p = subprocess.Popen(['python', location_of_module, db_file_obj['location']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdoutdata, stderrdata = p.communicate()
            # print stderrdata

            #if we get error data the module 'failed'
            module_passed = True
            if stderrdata:
                module_passed = False

            #process the output for printing to html
            output = self.processData(stdoutdata)
            #update the file with new module information
            output_obj[module] = output

            # set the processed module to passede or not
            self.modules[module] = module_passed

            #update our file in the database
        Database.db_update_malware_on_id(db_file_obj["_id"], output_obj)

        # put a timestamp on the process
        self.finish_process()
        Database.db_update_process(self.id, self.to_database_file())


class MultiProcer:
    def __init__(self, Database):
        self.cpu_count = mp.cpu_count()
        # self.cpu_count = 1
        self.Database = Database
        self.processes = []
        self.queue = Queue()

    def start(self):
        #TODO
        #could add process count so we don't always spin up 8 processes say

        self.processes = [mp.Process(target=self.run, args=(self.queue,)) for i in range(self.cpu_count)]
        for proc in self.processes:
            proc.start()
        # pool = mp.Pool(processes=4)
        # res= pool.apply_async(self.run)

    #TODO LOCKS
    def add_to_queue(self, process):
        self.queue.put(process)

    def pop_queue(self):
        return self.queue.get()

    def join_all():
        for proc in self.processes:
            proc.join()


    def run(self, q):
        # proc = mp.current_process()
        while(True):
            # if( q.empty()):
            #
            #     #TODO
            #     #not sure if this actually exits the process
            #
            #     print "DONE"
            #     return

            process = q.get()

            print process.file_name
            process.run(self.Database)




#CLASS to create process objects and run them
class Processor:
    def __init__(self, Database, Wizard):
        self.Wizard = Wizard
        self.modules = []       #all prossible modules we can run
        self.new_processes = [] #processes that need to be run still
        self.old_processes = [] #processes that have been run

        self.Multiproc = MultiProcer( Database)
        self.Multiproc.start()

        self.Database = Database

        self.is_running = False

    # for displaying all of the processes, already run or running
    def get_all_processes(self):
        return self.old_processes + self.new_processes

    def get_all_processes_db(self):
        process_stack = self.Database.db_get_all_processes()
        processes = self.process_stack_to_processes(process_stack, self.Database)
        return processes

    def process_stack_to_processes(self, db_process_stack, Database):
        processes = []
        for db_process in db_process_stack:

            file_id = db_process['file_id'];
            file = Database.db_find_by_id(file_id)

            process = Process(file['_id'], file['Name'])
            process.from_database_file(db_process)
            processes.append(process)

        return processes



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
            process.get_file_runs(self.Database)

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
            self.Database.db_proc_insert(process)

            #add the process to list of processes that still need to be processed
            self.new_processes.append(process)


    #auto_modules_config = {'module':True, 'module2':False}
    #NOTE NEED TO CHANGE BACK ONCE CONFIG CLASS IS IMPLEMENTED
    # def create_process_obj_auto(self, file, auto_modules_config):

    def create_process_obj_auto(self, files_array):
        for file in files_array:
            modules_array = self.Wizard.getModules()
            auto_modules_config = { x : True for x in modules_array }

            process = Process(file.id, file.filename)
            process.get_file_runs(self.Database)

            for module in auto_modules_config:
                if(auto_modules_config[module] == True):
                    process.add_module(module)

            #insert the process into the database
            self.Database.db_proc_insert(process)
            #add the process to list of processes that still need to be processed
            self.new_processes.append(process)
        self.run_modules(False)


    #processes the string data output of a processes
    def processData(self, data):
        retList = []
        aStr = ""
        # print data
        for c in data:

            if c == "\n":
                retList.append(aStr)
                # print aStr
                aStr = ""
            else:
                aStr += c

        return retList

    # runs the new processes
    #
    #   debug      - TRUE/FALSE wether or not to print module ouput to console
    #   Database   - globale database obj
    def run_modules(self, debug):
        #loop throug all curren new processees
        # if(self.is_running == False):
        #     self.is_running = True
        #     self.Multiproc.start()

        while self.new_processes:

            #remove the process
            process = self.new_processes.pop()

            self.Multiproc.add_to_queue(process)

        # self.MultiProcer.join_all()
