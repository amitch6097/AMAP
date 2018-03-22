# coding=utf-8
import sys
#trouble adding path so ...
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")
from bottle import static_file, run, template, get, redirect, request, route, template, auth_basic
import os
import zipfile
import json
import shutil

# need for other rat
import pefile
import pype32
import yara

# import run_modules
# import helper_functions
from dbio import Dbio
from processor import Processor
from uploader import MalwareUploader


Database = Dbio()
Uploader = MalwareUploader(os.path.dirname(os.path.realpath(__file__)))
Processor = Processor()

Database.db_clear()

@route('/')
def default():
    return template('login')

@route('/<name>')
def index(name):
    return template(name)


#MALWARE UPLOADING THINGS

@route('/file-rerun', method='POST')
def file_rerun():
    db_file = Database.db_find_by_id(request.forms.get('id'))

    Uploader.add_preloaded(db_file, Database)
    info = {'file_names' : Uploader.get_current_upload_filenames(), 'module_options': Processor.get_modules()}
    return template('process-modules', info)

@route('/file-upload')
def file_upload():

    #We have not chosen the modules for theses files so go to that page
    if Uploader.has_uploads():
        info = {'file_names' : Uploader.get_current_upload_filenames(), 'module_options': Processor.get_modules()}
        return template('process-modules', info)

    else:
        return template('file-upload')

@route('/upload', method='POST')
def do_upload():
    Uploader.upload(request.files.getall('upload'), Database)

    info = {'file_names' : Uploader.get_current_upload_filenames(), 'module_options': Processor.get_modules()}
    return template('process-modules', info)

@route('/process', method='POST')
def process_upload():

    Processor.create_process_obj(request.forms, Uploader.current_uploads, Database)
    Uploader.reset()
    Processor.run_modules(False, Database)

    return template('file-upload')

@route('/processes')
def load_processes():

    # IF PROCS WHERE LOADED FROM DB
    # db_procs = Database.db_get_all_processes()
    # Processor.db_proc_stack_to_processes()

    return template('processes', processes=Processor.get_all_processes())


# TODO db_list_one only gets the first file with name, is a problem for duplicates
@route('/file_view', method='POST')
def load_file():
    file_select = request.forms.get('filename')
    database_obj = Database.db_list_one('Name', file_select)
    del database_obj['location']

    return template('file-output', file_obj=database_obj)

# Static Routes
@get('/<filename:path>')
def static(filename):
    return static_file(filename, root='static/')


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


    return template('dashboard')


@route('/malware-search', method='POST')
def malware_search():
    search_input = request.forms.get('module-search-input')

    formated_objs = []
    search_ouput_objects = Database.db_find_first_char(search_input)
    for obj in search_ouput_objects:
        formated_objs.append(obj)

    return template('search', search_output=formated_objs)

@route('/my-modules')
def get_my_modules():
    modules = Processor.get_modules()
    return template('display-modules', modules=modules)

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



@route('/login-user', method="POST")
def login_page():
    username = request.forms.get('user_email')
    password = request.forms.get('password')
    print("Printing username: {}".format(username))
    print("Printing password: {}".format(password))
    return template('dashboard')


# run it
run(host='localhost', port=8080, reloder=True)

#@route('/')
#def check_password(user,password)
#check user/password here and return True/False

#@route('/')
#@auth_basic(check)
#def display_data():
#    return {'data': request.auth_basic}