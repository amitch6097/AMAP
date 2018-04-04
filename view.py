
# coding=utf-8
import sys
#trouble adding path so ...

#sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")
import gevent
from gevent import monkey; monkey.patch_all()
from bottle import static_file, run, template, get, redirect, request, route, template

import os
import zipfile
import json
import shutil
import datetime

# need for other rat
import pefile
import pype32
import yara
import time

from dbio import Database
from processor import Processor
from uploader import MalwareUploader
from file_watcher import FileGrab

# Wizard class for Background Analysis Platform
from wizard import Wizard

import multiprocessing as mp
import threading

Wizard = Wizard()
Uploader = MalwareUploader(os.path.dirname(os.path.realpath(__file__)))
Processor = Processor(Wizard)
FileGrab = FileGrab(Processor.create_process_obj_auto)

CWD = os.path.dirname(os.path.realpath(__file__))


# Database.db_clear()

@route('/')
def default():
    return template('login')

@route('/download/<filename:path>')
def d(filename):
    print filename
    return static_file(filename, root='modues/', download=True)

# #RUNS WHEN delete is selected on my modules page
# @route('/download-module')
# def download_my_module():
#     # modules_name = request.forms.get('module-name')
#     modules_name = 'sha1'
#     current_dir_path = os.path.dirname(os.path.realpath(__file__))
#
#     path = "{0}/modules/".format(current_dir_path)
#
#     if os.path.isdir(path):
#         shutil.rmtree(path)
#
#     return static_file(modules_name, root=path, download=True)

###########################
#TODO DELETE THESE ADD REAL BUTTONS

@route('/run-background')
def default():
    FileGrab.run()
    return template('login')

@route('/stop-background')
def default():
    FileGrab.stop()
    return template('login')

############################

@route('/<name>')
def index(name):
    return template(name)

@route('/wizard')
def wizard():
    #get info to display on next page
    info = {'module_options': Processor.get_modules(), 'running': Wizard.isRunning(), 'active_modules': Wizard.getModules(), 'time': Wizard.getTimeInterval(), 'numFiles': Wizard.getFileGrabInterval() }

    return template('wizard', info)

@route('/amap-active', method='POST')
def start_amap():
    buttonPressed = request.forms.get('enter')

    # Start Running AMAP
    if buttonPressed == "Submit":
        #set the wizard to running == True
        Wizard.startRunning()
        #set the selected modules
        Wizard.setModules(request.forms, Processor.get_modules())
        Wizard.setConfig(request.forms)
        Wizard.printConfig()

        # Run AMAP
        FileGrab.run(Wizard)

    # Return To Dashboard
    elif buttonPressed == "Return to Dashboard":
        return dash()

    # Quit Running AMAP
    elif buttonPressed == "Quit AMAP":
        Wizard.stopRunning()

        #Stop Running
        FileGrab.stop()


    #get info to display on next page
    info = {'module_options': Processor.get_modules(), 'running': Wizard.isRunning(), 'active_modules': Wizard.getModules(), 'time': Wizard.getTimeInterval(), 'numFiles': Wizard.getFileGrabInterval() }

    return template('wizard', info)



#MALWARE UPLOADING THINGS

#RUNS WHEN a start new process button is pressed on File View page
@route('/file-rerun', method='POST')
def file_rerun():
    db_file = Database.db_find_by_id(request.forms.get('id'))

    Uploader.add_preloaded(db_file, Database)
    info = {'file_names' : Uploader.get_current_upload_filenames(), 'module_options': Processor.get_modules()}
    return template('process-modules', info)

#RUNS WHEN file upload side bar button is Processed
# Decides which page to show file upload or process options
@route('/file-upload')
def file_upload():
    #We have files that need to be processed still
    if Uploader.has_uploads():
        info = {'file_names' : Uploader.get_current_upload_filenames(), 'module_options': Processor.get_modules()}
        return template('process-modules', info)

    #show file upload
    else:
        return template('file-upload')

#RUNS WHEN upload button is pressed on file upload packages
#Uploads the files and navigates to process options page
@route('/upload', method='POST')
def do_upload():

    #upload files
    files = request.files.getall('upload')
    Uploader.upload(files, Database)

    #get info to display on next page
    info = {'file_names' : Uploader.get_current_upload_filenames(), 'module_options': Processor.get_modules()}

    return template('process-modules', info)

#RUNS WHEN submit button is pressed on file upload module options page
@route('/process', method='POST')
def process_upload():
    Processor.create_process_obj(request.forms, Uploader.current_uploads)
    Uploader.reset()
    Processor.run_modules()
    return load_processes()


#RUNS WHEN processes sidebar option is pressed
@route('/processes')
def load_processes():
    try:
        processes = Processor.get_all_processes_db()
    except ProtocolError:
        processes = Processor.get_all_processes()

    return template('processes', processes=processes)


#RUNS WHEN a file is click on in either processes page or search_input
# TODO db_list_one only gets the first file with name, is a problem for duplicates
@route('/file_view', method='POST')
def load_file_view_post():

    #grab the selected file
    file_select = request.forms.get('filename')

    #grab a file with the same name
    database_obj = Database.db_list_one('Name', file_select)

    # used to not show location of the file on system
    #TODO could be deleted
    del database_obj['location']

    cuckoo_file_path = Processor.get_cuckoo(database_obj)

    return template('file-output', file_obj=database_obj)

# Static Routes
#USED for our CSS, JS and other assets
@get('/<filename:path>')
def static(filename):
    return static_file(filename, root='static/')

#RUNS WHEN a module is uploaded
# unzips the file and places it in modules folder
@route('/module-upload', method='POST')
def module_upload_post():
    uploads = request.files.getall('upload')
    uploads_name_array = []

    #TODO handle uploads with same names
    for upload in uploads:
        name, ext = os.path.splitext(upload.filename)
        assert ext == '.zip'


        # How to not allow file types
        # name, ext = os.path.splitext(upload.filename)
        # if ext not in ('.not', '.allowed', '.example'):
        #     return "File extension not allowed."

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


@route('/module-create', method='POST')
def module_create_post():
    text = request.forms.get('code-text-input')
    module_name = request.forms.get('module-name')

    module_name = module_name.split(".")[0]


    save_path = os.path.join(CWD, "modules", module_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    full_name = module_name + ".py"
    file_path = os.path.join(save_path, full_name)
    file = open(file_path, "w")
    file.write(text)
    print text

    return get_my_modules()

#RUNS WHEN search button is pressed
#grabs input from search bar and searches database for those chars
@route('/malware-search', method='POST')
def malware_search():

    search_input = request.forms.get('module-search-input')

    formated_objs = []

    search_ouput_objects = Database.db_find_first_char(search_input)
    for obj in search_ouput_objects:
        formated_objs.append(obj)

    return template('search', search_output=formated_objs)


@route('/my-modules-creator', method='POST')
def my_module_creator_post():
    module_name = request.forms.get("module-name")
    file_contents = []

    if module_name == None:
        file_contents = ['import os', 'from optparse import OptionParser', '', '', '__description__ =', '__author__ =', "__version__ = '1.0'", '__date__ =', '', 'def my_module(filename):', '', 'if __name__ == "__main__":', "        parser = OptionParser(usage='usage: %prog file / dir\\n' + __description__, version='%prog ' + __version__)", '        (options, args) = parser.parse_args()', '        is_file = os.path.isfile(args[0])', '        if is_file:', '            my_module(args[0])']
        return template('module-creator', {"module_name":"", "file_contents":file_contents})

    path = "{0}/modules/{1}".format(CWD, module_name)
    full_name = "{0}.py".format(module_name)
    file_path = os.path.join(path, full_name)

    try:
        with open(file_path, 'r') as fp:
            for line in fp:
                file_contents.append(line.rstrip())
    except:
        file_contents = []

    return template('module-creator', {"module_name":full_name, "file_contents":file_contents})

#RUNS WHEN my modules is selected
#shows the current uploaded modules
@route('/my-modules')
def get_my_modules():
    modules = Processor.get_editable_modules()
    return template('display-modules', modules=modules)

#RUNS WHEN delete is selected on my modules page
@route('/delete-module', method='POST')
def delete_modules_post():
    modules_name = request.forms.get('module-name')

    path = "{0}/modules/{1}".format(CWD, modules_name)

    if os.path.isdir(path):
        shutil.rmtree(path)

    return get_my_modules()

@route('/dashboard')
def dash():
    #db_list = Database.db_list_all_time()
    #print(db_list)
    from_DB = Database.db_list_malwaredate()
    malware_count = 0
    for i in from_DB:
        print(i["Time"])
        malware_count += 1
    procset = Database.db_list_avgproctime()
    avg_time = 0
    total_time = 0
    av_count = 0
    newnmal = Database.db_get_count()- malware_count
    if newnmal < 0:
        newnmal = malware_count+3
    for av in procset:
        total_time += av["ATime"]
        av_count += 1
    if av_count is 0:
        avg_time = 0
    else:
        avg_time = total_time/(av_count-1)
    print(total_time,'/',av_count,'=',avg_time)
    info = {'new_mal' : malware_count, 'new_nmal': newnmal, 'avg_time' : datetime.datetime.utcfromtimestamp(avg_time).strftime("%S.%f")}
    return template('dashboard', info)


@route('/login-user', method="POST")
def login_page():
    username = request.forms.get('user_email')
    password = request.forms.get('password')
    print("Printing username: {}".format(username))
    print("Printing password: {}".format(password))
    return dash()


# run it
run(host='0.0.0.0', port=8080, server='gevent', debug=True)
