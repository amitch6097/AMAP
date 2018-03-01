import multiprocessing as mp
import os
import subprocess
import sys
from time import gmtime, strftime

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

class Process:
    def __init__(self, f):
        self.file = f
        self.modules = {}
        self.percent_done = 0
        self.start_time = "idle"
        self.end_time = "waiting..."
        self.run_number = -1
        self.id = -1

    def edit_id(self, id):
        self.id = id

    def add_module(self, module, on_off):
        self.modules[module] = on_off

    def print_modules(self):
        for key in self.modules:
            print "KEY:{0} VALUE:{1}".format(key, self.modules[key])

    def finish_process(self):
        self.percent_done = 100
        self.end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def start_process(self):
        self.start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.end_time = "running..."

    def get_file_runs(self, Database):
        assert self.file.id != -1
        self.run_number = Database.db_inc_runs_by_id(self.file.id)
        self.file.runs = self.run_number

    def to_database_file(self):
        return {'file_id':self.file.id,
            "filename":self.file.filename,
             "modules":self.modules,
             "run_number":self.run_number,
             "start_time":self.start_time,
             "end_time":self.end_time,
             }


class Processor:
    def __init__(self):
        self.modules = []
        self.new_processes = []
        self.old_processes = []

    def get_all_processes(self):
        return self.old_processes + self.new_processes


    def get_modules(self):
        self.modules = []

        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        modules_folder = "{0}/modules".format(current_dir_path)

        for file_or_dir in os.listdir(modules_folder):
            if os.path.isdir("{0}/{1}".format(modules_folder, file_or_dir)):
                self.modules.append(file_or_dir)

        self.modules = [x for x in self.modules if x != "__MACOSX"]

        return self.modules

    def create_process_obj(self, forms, uploaded_malware_array, Database):

        for current_file in uploaded_malware_array:
            process = Process(current_file)
            process.get_file_runs(Database)

            for index, module in enumerate(self.modules):
                name = "{0}_{1}".format(current_file.filename, index)
                checkbox = forms.get(name)

                if (checkbox == 'on'):
                    process.add_module(module, False)

            Database.db_proc_insert(process)
            self.new_processes.append(process)

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

    def run_modules(self, debug, Database):
        while self.new_processes:
            process = self.new_processes.pop()
            process.start_process()

            cwd = os.getcwd()

            output_obj = process.file.to_database_file()

            for module in process.modules:

                location_of_module = '{0}/modules/{1}/{1}.py'.format(cwd, module)

                 # PRINT OUTPUT TO CONSOLE
                if debug==True:
                    p = subprocess.Popen(['python', location_of_module, process.process.file.path])

                else:
                    p = subprocess.Popen(['python', location_of_module, process.file.path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdoutdata, stderrdata = p.communicate()
                    print stderrdata

                    module_passed = True
                    if stderrdata:
                        module_passed = False

                    output = self.processData(stdoutdata)
                    output_obj[module] = output

                    process.modules[module] = module_passed

                    Database.db_update_on_id(process.file.id, output_obj)


            process.finish_process()

            process = self.old_processes.append(process)

        # return output_obj
