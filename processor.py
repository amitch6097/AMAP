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
        self.finished = False
        self.percent_done = 0
        self.start_time = "idle"
        self.end_time = "waiting..."


    def add_module(self, module, on_off):
        self.modules[module] = on_off

    def print_modules(self):
        for key in self.modules:
            print "KEY:{0} VALUE:{1}".format(key, self.modules[key])

    def finish_process(self):
        self.finished = True
        self.percent_done = 100
        self.end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def start_process(self):
        self.start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.end_time = "running..."



class Processor:
    def __init__(self):
        self.modules = []
        self.processes = []

    def get_modules(self):
        self.modules = []

        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        modules_folder = "{0}/modules".format(current_dir_path)

        for file_or_dir in os.listdir(modules_folder):
            if os.path.isdir("{0}/{1}".format(modules_folder, file_or_dir)):
                self.modules.append(file_or_dir)
        return self.modules

    def create_process_obj(self, forms, uploaded_malware_array):

        for current_file in uploaded_malware_array:
            process = Process(current_file)

            for index, module in enumerate(self.modules):
                name = "{0}_{1}".format(current_file.filename, index)
                checkbox = forms.get(name)

                process.add_module(module, (checkbox == 'on'))

            self.processes.append(process)

    def processData(self, data):
        retList = []
        aStr = ""
        for c in data:
            if c == "\n":
                retList.append(aStr)
                aStr = ""
            else:
                aStr += c

        return retList

    def run_modules(self, debug, Database):
        for process in self.processes:
            process.start_process()
            cwd = os.getcwd()

            output_obj = {"Name":process.file.filename, "location":process.file.path}


            for module in process.modules:
                if process.modules[module] == False:
                    continue

                location_of_module = '{0}/modules/{1}/{1}.py'.format(cwd, module)

                 # PRINT OUTPUT TO CONSOLE
                if debug==True:
                    p = subprocess.Popen(['python', location_of_module, process.process.file.path])

                else:
                    p = subprocess.Popen(['python', location_of_module, process.file.path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdoutdata, stderrdata = p.communicate()

                    output = self.processData(stdoutdata)
                    output_obj[module] = output

            process.finish_process()
            Database.db_insert(output_obj)

        return output_obj
