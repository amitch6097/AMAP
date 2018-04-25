import sys
from gevent import monkey; monkey.patch_all()
from bottle import static_file, run, template, get, redirect, request, route, template, abort

import os
import zipfile
import json
import shutil
import datetime

import pefile
import pype32
import yara
import time

import multiprocessing as mp
import threading

from dbio import Database
from processor import Processor
from uploader import MalwareUploader
from file_watcher import FileGrab
from wizard import Wizard

Wizard = Wizard()
Uploader = MalwareUploader(os.path.dirname(os.path.realpath(__file__)))
Processor = Processor(Wizard)
FileGrab = FileGrab(Processor.create_process_obj_auto)

CWD = os.path.dirname(os.path.realpath(__file__))


"""default is login page"""
@route('/')
def default():
    return login()

"""login with warning based on password/uesrname"""
@route('/login')
def login():
    return template('login', {"warning":""})

"""for donwloading a staticfile"""
@route('/download/<filename:path>')
def d(filename):
    return static_file(filename, root="CuckooReports/", download=True)


@route('/<name>')
def index(name):
    return template(name)

"""displays the wizard with options from the wizard class"""
@route('/_wizard', "GET")
def wizard():
    #get info to display on next page
    info = {'module_options': Processor.get_modules(), 'running': Wizard.isRunning(), 'active_modules': Wizard.getModules(), 'time': Wizard.getTimeInterval(), 'numFiles': Wizard.getFileGrabInterval() }
    return template('_wizard', info)

"""post to activate the amap wizard"""
@route('/_amap-active', method='POST')
def start_amap_jquery():

    #set the wizard to running
    Wizard.startRunning()

    #set the selected modules
    Wizard.setModules(request.forms, Processor.get_modules())
    Wizard.setConfig(request.forms)
    Wizard.printConfig()

    # Run AMAP
    FileGrab.run(Wizard)

    #get info to display on next page
    info = {'module_options': Processor.get_modules(), 'running': Wizard.isRunning(), 'active_modules': Wizard.getModules(), 'time': Wizard.getTimeInterval(), 'numFiles': Wizard.getFileGrabInterval() }

    return template('_wizard', info)

"""post to quit the amap wizard"""
@route('/_amap-quit', method='POST')
def quit_amap_jquery():

    #set the wizard to not running
    Wizard.stopRunning()

    #Stop Running
    FileGrab.stop()

    #get info to display on next page
    info = {'module_options': Processor.get_modules(), 'running': Wizard.isRunning(), 'active_modules': Wizard.getModules(), 'time': Wizard.getTimeInterval(), 'numFiles': Wizard.getFileGrabInterval() }

    return template('_wizard', info)

"""sets a previously uploaded file to rerun"""
@route('/_file-rerun', method='POST')
def file_rerun():

    #grab file from dabatase using post form
    db_file = Database.db_find_by_id(request.forms.get('id'))
    #add to uploads
    Uploader.add_preloaded(db_file, Database)
    #get options for modules
    info = {'file_names' : Uploader.get_current_upload_filenames(), 'module_options': Processor.get_modules()}

    return template('_process-modules', info)

"""uploades files to the system"""
@route('/_upload_files', method='POST')
def file_upload_jquery():

    #grab files from post form
    files = request.files.getall('files[]')
    #upload to system
    Uploader.upload(files, Database)
    #get info to display modules
    info = {'file_names' : Uploader.get_current_upload_filenames(), 'module_options': Processor.get_modules()}
    return template('_process-modules', info)

"""starts the processing of files that have been uploaded"""
@route('/_process', method='POST')
def process_upload():
    #create process object from the uploaders uploads
    Processor.create_process_obj(request.forms, Uploader.current_uploads)
    Uploader.reset()

    #run the processes
    Processor.run_modules()
    return template("_file-upload")

"""gets all running and past processes to display"""
@route('/_processes', method="GET")
def load_processes():
    processes = Processor.get_all_processes()
    return template('_processes', processes=processes)

"""gets the view for a file with all module ouput"""
@route('/_file_view', method='POST')
def load_file_view_post():

    #grab the selected file from the post form
    file_select = request.forms.get('filename')

    #grab a file with the same name
    database_obj = Database.db_list_one('Name', file_select)

    #remove the location from modules
    del database_obj['location']
    database_obj["time"] = database_obj["time"]

    #grab cuckoo report if avaiable
    cuckoo_file_path = Processor.get_cuckoo(database_obj)

    return template('_file-output', file_obj=database_obj)

"""static routes for css, js, and html"""
@get('/<filename:path>')
def static(filename):
    return static_file(filename, root='static/')


"""unzips an uploaded module and adds it to the list of modules"""
@route('/_module-upload', method='POST')
def module_upload_post():
    uploads = request.files.getall('files[]')
    uploads_name_array = []
    print uploads
    for upload in uploads:
        print upload.filename
        name, ext = os.path.splitext(upload.filename)
        assert ext == '.zip'

        # set up downloads path
        save_path = "{path}/modules".format(path=CWD)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path, overwrite=True)

        zip_ref = zipfile.ZipFile(file_path, 'r')
        zip_ref.extractall(save_path)
        zip_ref.close()

        os.remove(file_path)

    return get_my_modules()

"""creates a new module from the module creator"""
@route('/module-create', method='POST')
def module_create_post():

    # get the code created in module creator
    text = request.forms.get('code-text-input')
    #get the name the file is to be saved as
    module_name = request.forms.get('module-name')
    module_name = module_name.split(".")[0]

    #write to and save the module from the form info
    save_path = os.path.join(CWD, "modules", module_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    full_name = module_name + ".py"
    file_path = os.path.join(save_path, full_name)
    file = open(file_path, "w")
    file.write(text)

    return get_my_modules()


"""searches the database for malware similar to search settings"""
@route('/_malware-search', method='POST')
def malware_search():

    # greab form input
    search_input = request.forms.get('module-search-input')
    type_input = request.forms.get('malware-search-type').rstrip().lstrip()

    #grab the type of search we want
    type_converter_dic = {
        "File Name" : "Name",
        "MD5": "md5",
        "SHA1" :"sha1",
        "SHA256": "sha256"
    }
    if(type_input in type_converter_dic.keys()):
        type = type_converter_dic[type_input]
    else:
        type = "Name"

    #setup array for return from search
    formated_objs = []
    #search in database
    search_ouput_objects = Database.db_find_malware_hash(search_input, type)
    #add to ouput array
    for obj in search_ouput_objects:
        formated_objs.append(obj)

    return template('_search', search_output=formated_objs)

"""returns to view for module creator when edit or create new module is pressed"""
@route('/_my-modules-creator', method='POST')
def my_module_creator_get():

    #try to find the module name and file to edit
    try:
        module_name = request.forms.get("module-name")
    except NameError:
        module_name = ''

    file_contents = []

    #if we can not find a file create a template file
    if module_name == None:
        file_contents = ['import os', 'from optparse import OptionParser', '', '', '__description__ =', '__author__ =', "__version__ = '1.0'", '__date__ =', '', 'def my_module(filename):', '', 'if __name__ == "__main__":', "        parser = OptionParser(usage='usage: %prog file / dir\\n' + __description__, version='%prog ' + __version__)", '        (options, args) = parser.parse_args()', '        is_file = os.path.isfile(args[0])', '        if is_file:', '            my_module(args[0])']
        return template('_module-creator', {"module_name":"", "file_contents":file_contents})

    # otherwise return the file contents that was given to us
    path = "{0}/modules/{1}".format(CWD, module_name)
    full_name = "{0}.py".format(module_name)
    file_path = os.path.join(path, full_name)


    #try to open the file and read the contents
    try:
        with open(file_path, 'r') as fp:
            for line in fp:
                file_contents.append(line.rstrip())

    #other wise the file is considered empty
    except:
        file_contents = []

    return template('_module-creator', {"module_name":full_name, "file_contents":file_contents})

"""returns to view for all of the current modules"""
@route('/_my-modules', "GET")
def get_my_modules():
    # only show editable modules
    modules = Processor.get_editable_modules()
    return template('_display-modules', modules=modules)


"""deletes a module from a form post"""
@route('/_delete-module', method='POST')
def delete_module_post():
    # grab the name of the module to delete
    modules_name = request.forms.get('module-name')
    #get the path
    path = "{0}/modules/{1}".format(CWD, modules_name)
    #remove the tree structor
    if os.path.isdir(path):
        shutil.rmtree(path)

    return {}
"""Gets all of the processor data and puts it into a json obj"""
@route('/_processes_data', "GET")
def load_processes_data_jquery():
    processes = Processor.get_all_processes()

    arr = []
    for process in processes:
        arr.append(process.to_database_file_html())

    return json.dumps({"processes":arr})

"""Retrives the data fror the dashboard"""
@route('/_dash_data', "GET")
def add_numbers():
    from_DB = Database.db_list_malwaredate()
    malware_count = 0
    C1V0 = 0
    C1V1 = 0
    C1V2 = 0
    C1V3 = 0
    C1V4 = 0
    C1V5 = 0
    for i in from_DB:
        if (i["Time"] > (time.time()-3600)):
            C1V0 += 1
        elif (i["Time"] < (time.time()-3600) and i["Time"] > (time.time()-7200)):
            C1V1 += 1
        elif (i["Time"] < (time.time()-7200) and i["Time"] > (time.time()-10800)):
            C1V2 += 1
        elif (i["Time"] < (time.time()-10800) and i["Time"] > (time.time()-14400)):
            C1V3 += 1
        elif (i["Time"] < (time.time()-14400) and i["Time"] > (time.time()-18000)):
            C1V4 += 1
        elif (i["Time"] < (time.time()-18000) and i["Time"] > (time.time()-21600)):
            C1V5 += 1
        malware_count += 1
    from_DB_newmw = Database.db_gui_get_newmw()
    nmw_count = 0
    C2V0 = 0
    C2V1 = 0
    C2V2 = 0
    C2V3 = 0
    C2V4 = 0
    C2V5 = 0
    for j in from_DB_newmw:
        if (j["NTime"] > (time.time()-3600)):
            C2V0 += 1
        elif (j["NTime"] < (time.time()-3600) and j["NTime"] > (time.time()-7200)):
            C2V1 += 1
        elif (j["NTime"] < (time.time()-7200) and j["NTime"] > (time.time()-10800)):
            C2V2 += 1
        elif (j["NTime"] < (time.time()-10800) and j["NTime"] > (time.time()-14400)):
            C2V3 += 1
        elif (j["NTime"] < (time.time()-14400) and j["NTime"] > (time.time()-18000)):
            C2V4 += 1
        elif (j["NTime"] < (time.time()-18000) and j["NTime"] > (time.time()-21600)):
            C2V5 += 1
    procset = Database.db_list_avgproctime()
    avg_time = 0
    total_time = 0
    av_count = 0
    newnmal = Database.db_get_count()- malware_count
    if newnmal < 0:
        newnmal = malware_count+3
    for av in procset:
	if av["ATime"] > 0:
        	total_time += av["ATime"]
        	av_count += 1
    if av_count is 0:
        avg_time = 0
    else:
        avg_time = total_time/(av_count)

    types = Database.db_gui_get_newtype()
    exe = 0
    other = 0
    for k in types:
        if ("exe" in k["Type"]):
            exe += 1
        else:
            other += 1
    total = exe + other
    if total is not 0:
        exe_percent = 100*(exe/float(exe+other))
        other_percent = 100-exe_percent
    else:
        exe_percent = 0
        other_percent = 0

    info = {'new_mal' : malware_count, 'new_nmal': total-malware_count, 'avg_time' : datetime.datetime.utcfromtimestamp(avg_time).strftime("%S.%f"), 'C1V0':C1V0, 'C1V1':C1V1, 'C1V2':C1V2, 'C1V3':C1V3, 'C1V4':C1V4, 'C1V5':C1V5, 'C2V0':C2V0, 'C2V1':C2V1, 'C2V2':C2V2, 'C2V3':C2V3, 'C2V4':C2V4, 'C2V5':C2V5, 'PI1':exe, 'PI2':other, 'T0':datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M"), 'T1':datetime.datetime.fromtimestamp(time.time()-3600).strftime("%H:%M"), 'T2':datetime.datetime.fromtimestamp(time.time()-7200).strftime("%H:%M"), 'T3':datetime.datetime.fromtimestamp(time.time()-10800).strftime("%H:%M"), 'T4':datetime.datetime.fromtimestamp(time.time()-14400).strftime("%H:%M"), 'T5':datetime.datetime.fromtimestamp(time.time()-18000).strftime("%H:%M")}

    return json.dumps(info)

"""Retrives the single page application"""
@route('/dashboard')
def index():
    return template('single-page')

"""Logs a user in before returning to the dashboard"""
@route('/login-user', method="POST")
def login_page():
    username = request.forms.get('user_email')
    password = request.forms.get('password')

    if(username == ""):
        return template('login', {"warning":"Wrong Username"})
    if(password == ""):
        return template('login', {"warning":"Wrong Password"})

    print("Printing username: {}".format(username))
    print("Printing password: {}".format(password))
    return index()

# run it
run(host='0.0.0.0', port=8080, server='gevent', debug=True)
