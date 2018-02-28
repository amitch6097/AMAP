# coding=utf-8
import sys
#trouble adding path so ...
#sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/")
from bottle import static_file, run, template, get, redirect, request, route, template
import os
import zipfile
import json

import run_modules
# import helper_functions
from dbio import Dbio
from processor import Processor
from uploader import MalwareUploader


Database = Dbio()
Uploader = MalwareUploader(os.path.dirname(os.path.realpath(__file__)))
Processor = Processor()
# Database.db_del_element('Name', 'scraper_2_rutgers.py')
# Database.db_del_element('Name', 'scraper_2_rutgers.py')


@route('/')
def default():
    return template('login')

@route('/<name>')
def index(name):
    return template(name)


#MALWARE UPLOADING THINGS

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
    Uploader.upload(request.files.getall('upload'))

    info = {'file_names' : Uploader.get_current_upload_filenames(), 'module_options': Processor.get_modules()}
    return template('process-modules', info)

@route('/process', method='POST')
def process_upload():

    Processor.create_process_obj(request.forms, Uploader.current_uploads)
    Uploader.reset()
    Processor.run_modules(False, Database)

    return template('file-upload')

@route('/processes')
def load_processes():
    return template('processes', processes=Processor.processes)

@route('/file_view', method='POST')
def load_file():
    file_select = request.forms.get('filename')
    database_obj = Database.db_list_one('Name', file_select)

    return template('file-output', file_obj=database_obj)

# Static Routes
@get('/<filename:path>')
def static(filename):
    return static_file(filename, root='static/')


#TODO build out
@route('/module-upload', method='POST')
def servo_pos():
    current_dir_path = os.path.dirname(os.path.realpath(__file__))

    # grab uploaded file from form
    # upload = request.files.get('upload')

    uploads = request.files.getall('upload')
    uploads_name_array = []

    #TODO handle uploads with same names
    for upload in uploads:
        print upload.filename

        # How to not allow file types
        # name, ext = os.path.splitext(upload.filename)
        # if ext not in ('.not', '.allowed', '.example'):
        #     return "File extension not allowed."

        # set up downloads path
        save_path = "{path}/RatDecoders".format(path=current_dir_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)


        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path, overwrite=True) #overwrite TRUE might not be good?

        # add to array of names
        uploads_name_array.append(upload.filename)

    info = {'file_names' : uploads_name_array}


    return template('modules', info)


@route('/malware-search', method='POST')
def malware_search():
    search_input = request.forms.get('module-search-input')

    formated_objs = []
    search_ouput_objects = Database.db_find_first_char(search_input)
    for obj in search_ouput_objects:
        formated_objs.append(obj)

    return template('search', search_output=formated_objs)

@route('/upload-module', method='POST')
def upload_module():
    file_name = request.forms.get('file_name')
    file_location = "RatDecoders/{file_name}".format(file_name=file_name)

    path_to_zip_file = file_location
    directory_to_extract_to = "RatDecoders"

    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()

    return template('dashboard')



@route('/login', method="POST")
def login_page():
    username = request.forms.get('user_email')
    password = request.forms.get('password')
    print("Printing username: {}".format(username))
    print("Printing password: {}".format(password))
    return template('dashboard')
# run it
run(host='localhost', port=8080)
