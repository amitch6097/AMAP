import multiprocessing as mp
import os
import subprocess
import sys
from time import gmtime, strftime

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
    def __init__(self, file):
        self.file = file
        self.file_id =  file.id
        self.file_name = file.filename

        #modules is a dictionary w/
        # {'module name': wether or not module passed/ran}
        # Ex {'ratDecoder':False} -> ratDecoder failed to run on file
        self.modules = {}

        self.percent_done = 0
        self.start_time = "idle"
        self.end_time = "waiting..."
        self.run_number = -1
        self.id = -1

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
        assert self.file.id != -1
        self.run_number = Database.db_inc_runs_by_id(self.file.id)
        self.file.runs = self.run_number


    #for putting the process into the database
    def to_database_file(self):
        return {'file_id':self.file.id,
            "filename":self.file.filename,
             "modules":self.modules,
             "run_number":self.run_number,
             "start_time":self.start_time,
             "end_time":self.end_time,
             }
    def from_database_file(self, db_file):
        self.file.id = db_file['file_id']
        self.file.filename = db_file["filename"]
        self.modules = db_file["modules"]
        self.run_number = db_file["run_number"]
        self.start_time = db_file["start_time"]
        self.end_time = db_file["end_time"]

#CLASS to create process objects and run them
class Processor:
    def __init__(self):
        self.modules = []       #all prossible modules we can run
        self.new_processes = [] #processes that need to be run still
        self.old_processes = [] #processes that have been run

    # for displaying all of the processes, already run or running
    def get_all_processes(self):
        return self.old_processes + self.new_processes

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

        return self.modules

    #creates a process object from a form and uploads
    #
    #   forms                  - a form submitted through a post action
    #   uploaded_malware_array - array of Malware Objects see Uploader.py
    #   Database               - our global database object
    def create_process_obj(self, forms, uploaded_malware_array, Database):

        #loop through malware objects
        for current_file in uploaded_malware_array:
            #create a process object from it
            process = Process(current_file)
            # get the nummber of times the file has been run
            process.get_file_runs(Database)

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

    def db_proc_stack_to_processes(db_proc_stack, Database):
        for proc in db_proc_stack:

            file_id = proc['file_id'];
            File = Database.db_find_by_id(file_id)

            from_database_file



    #processes the string data output of a processes
    def processData(self, data):
        retList = []
        aStr = ""
        print data
        for c in data:
            if c == "\n":
                retList.append(aStr)
                aStr = ""
            else:
                aStr += c

        return retList

    # runs the new processes
    #
    #   debug      - TRUE/FALSE wether or not to print module ouput to console
    #   Database   - globale database obj
    def run_modules(self, debug, Database):

        #loop throug all curren new processees
        while self.new_processes:

            #remove the process
            process = self.new_processes.pop()
            #put a timestamp on it
            process.start_process()

            cwd = os.getcwd()

            # grab the file out of the databse because
            #we are updating the information on the file
            # output_obj = process.file.to_database_file()
            db_file_obj = Database.db_find_by_id(process.file_id)
            output_obj = []

            for module in process.modules:

                #location main python file in modules folder on system
                location_of_module = '{0}/modules/{1}/{1}.py'.format(cwd, module)

                 # PRINT OUTPUT TO CONSOLE
                if debug==True:
                    p = subprocess.Popen(['python', location_of_module, db_file_obj['location']])

                else:
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
                    process.modules[module] = module_passed

                    #update our file in the database
                    Database.db_update_malware_on_id(db_file_obj["_id"], output_obj)

            # put a timestamp on the process
            process.finish_process()

            #put the process in old, so we can still show it
            process = self.old_processes.append(process)
            Database.db_update_process(process)

        # return output_obj
