
# coding=utf-8
import sys
#trouble adding path so ...
<<<<<<< HEAD
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")
from bottle import static_file, run, template, get, redirect, request, route, template, auth_basic
=======

#sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")
import gevent
from gevent import monkey; monkey.patch_all()
from bottle import static_file, run, template, get, redirect, request, route, template

>>>>>>> 33bb2a17b9dc970e77973b68d6f8d2defc263a24
import os
import zipfile
import json
import shutil

# need for other rat
import pefile
import pype32
import yara
import time

# import run_modules
# import helper_functions
from dbio import Dbio
from processor import Processor
from uploader import MalwareUploader
from passlib.apps import custom_app_context as pwd_context
from beaker.middleware import SessionMiddleware
# from file_watcher import Watcher
from file_watcher import FileGrab

# Wizard class for Background Analysis Platform
from wizard import Wizard


import multiprocessing as mp
import threading


Wizard = Wizard()

Database = Dbio()
Uploader = MalwareUploader(os.path.dirname(os.path.realpath(__file__)))
Processor = Processor(Database, Wizard)

# def file_process_callback(files):
#     for file in files:
#         print file

FileGrab = FileGrab(Database, Processor.create_process_obj_auto)

# watcher_process = mp.Process(target=FileGrab.run)
# watcher_process.daemon = True
# watcher_process.start()

#WATCH DOG STUFF THAT DOESN'T WORK
# Watcher = Watcher()
# def print_something(event):
#     print "This"
#     if event.is_directory:
#         return None
#
#     elif event.event_type == 'created':
#         # Take any action here when a file is first created.
#         print "Received created event - %s." % event.src_path
#
#     elif event.event_type == 'modified':
#         # Taken any action here when a file is modified.
#         print "Received modified event - %s." % event.src_path
# Watcher.run(print_something)
# watcher_process = mp.Process(target=Watcher.run, args=(print_something,))
# watcher_process.daemon = True
# watcher_process.start()

# NOTE HANGS FOREVER
# gevent.spawn(Watcher.run, print_something)

Database.db_clear()

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
    print name
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

    #make process objects from page information and uploads
    Processor.create_process_obj(request.forms, Uploader.current_uploads)

    #reset uploader so that we can upload more files
    Uploader.reset()

    # run the process objects we just created
    # Processor.run_modules(False, Database)
    Processor.run_modules(False)

    # return to the base page
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
def load_file():

    #grab the selected file
    file_select = request.forms.get('filename')

    #grab a file with the same name
    database_obj = Database.db_list_one('Name', file_select)

    # used to not show location of the file on system
    #TODO could be deleted
    del database_obj['location']
    print database_obj
    # del database_obj['cuckoo_id']

    return template('file-output', file_obj=database_obj)

# Static Routes
#USED for our CSS, JS and other assets
@get('/<filename:path>')
def static(filename):
    return static_file(filename, root='static/')

#RUNS WHEN a module is uploaded
# unzips the file and places it in modules folder
@route('/module-upload', method='POST')
def servo_pos():
    current_dir_path = os.path.dirname(os.path.realpath(__file__))

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
        save_path = "{path}/modules".format(path=current_dir_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)


        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path, overwrite=True) #overwrite TRUE might not be good?

        # new_dir = "{0}/{1}".format(save_path, name)
        # os.makedirs(new_dir)

        zip_ref = zipfile.ZipFile(file_path, 'r')
        zip_ref.extractall(save_path)
        zip_ref.close()

        os.remove(file_path)

        # mac_created_folder = "{0}/__MACOSX".format(save_path)
        # if os.path.isdir(mac_created_folder):
        #     shutil.rmtree(mac_created_folder)


    return dash()


@route('/module-create', method='POST')
def servo_pos():
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    text = request.forms.get('')


    return dash()

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

#RUNS WHEN my modules is selected
#shows the current uploaded modules
@route('/my-modules')
def get_my_modules():

    modules = Processor.get_modules()
    return template('display-modules', modules=modules)

#RUNS WHEN delete is selected on my modules page
@route('/delete-module', method='POST')
def get_my_modules():
    modules_name = request.forms.get('module-name')
    current_dir_path = os.path.dirname(os.path.realpath(__file__))

    path = "{0}/modules/{1}".format(current_dir_path,modules_name)

    if os.path.isdir(path):
        shutil.rmtree(path)

    modules = Processor.get_modules()
    return template('display-modules', modules=modules)


# @route('/upload-module', method='POST')
# def upload_module():
#     file_name = request.forms.get('file_name')
#     file_location = "modules/{file_name}".format(file_name=file_name)
#
#     path_to_zip_file = file_location
#     directory_to_extract_to = "modules"
#
#     zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
#     zip_ref.extractall(directory_to_extract_to)
#     zip_ref.close()
#
#     # os.remove(path_to_zip_file)
#
#     return template('dashboard')


@route('/dashboard')
def dash():
    #db_list = Database.db_list_all_time()
    #print(db_list)
    from_DB = Database.db_list_malwaredate()
    malware_count = 0
    for i in from_DB:
        print(i["Time"])
        malware_count += 1
    info = {'new_mal' : malware_count, 'new_nmal': Database.db_get_count()- malware_count, 'avg_time' : 3.5}
    return template('dashboard', info)


@route('/login-user', method="POST")
def login_page():
    username = request.forms.get('user_email')
    password = request.forms.get('password')
    if username == "" or password == "":
        return {"error":"These can't be blank"}

    user = users.find_one({"Username":username})
    if user is None:
        return {"error":"%s is not a valid user" %(username)}
    if pwd_context.verify(password, user['pwdhash']):
        #Success, let's set the session and send them back to the dashboard
        success = bottle.request.environ.get('beaker.session')
        success['logged_in'] = True
        success['username'] = username
        redirect("/")
    else:
        return {"error":"Incorrect password"}
    print("Printing username: {}".format(username))
    print("Printing password: {}".format(password))
<<<<<<< HEAD
    Databse.db_verify_login(username,password)
    return template('dashboard')
=======
    db_list = Database.db_list_all_time()
    print(db_list)
    info = {'processed_day' : Database.db_get_count(), 'new_sample': Database.db_get_count(), 'avg_time' : 3.5}
    return template('dashboard', info)
>>>>>>> 33bb2a17b9dc970e77973b68d6f8d2defc263a24

@route('/logout', method=['GET'])
def handle_logout():
    success = bottle.request.environ.get('beaker.session')
    success.invalidate()
    redirect("/")


# run it
<<<<<<< HEAD
run(host='localhost', port=8080, reloder=True)

#@route('/')
#def check_password(user,password)
#check user/password here and return True/False

#@route('/')
#@auth_basic(check)
#def display_data():
#    return {'data': request.auth_basic}
=======
run(host='0.0.0.0', port=8080, server='gevent')
>>>>>>> 33bb2a17b9dc970e77973b68d6f8d2defc263a24
