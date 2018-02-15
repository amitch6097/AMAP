
import sys
#trouble adding path so ...
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/")

import os
from bottle import static_file, run, template, get, redirect, request, route, template

# import our modules
sys.path.insert(0, 'modules/')
from static_type import filetype_module
from static_hashes import sha1_module, md5_module

@route('/')
def default():
    return template('dashboard')
    # return redirect('/index.html')

@route('/<name>')
def index(name):
    return template(name)
    # return static_file(name, root="static/")

# # Static Routes
@get('/<filename:path>')
def static(filename):
    return static_file(filename, root='static/')

@route('/upload', method='POST')
def do_upload():
    current_dir_path = os.path.dirname(os.path.realpath(__file__))

    # grab uploaded file from form
    # upload = request.files.get('upload')

    uploads = request.files.getall('upload')
    uploads_name_array = []

    for upload in uploads:
        print upload.filename

        # How to not allow file types
        # name, ext = os.path.splitext(upload.filename)
        # if ext not in ('.not', '.allowed', '.example'):
        #     return "File extension not allowed."

        # set up downloads path
        save_path = "{path}/downloads".format(path=current_dir_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)


        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path)

        # add to array of names
        uploads_name_array.append(upload.filename)

    info = {'file_names' : uploads_name_array}

    # return "File successfully saved to '{0}'.".format(save_path)
    return template('process-modules', info)

@route('/process', method='POST')
def process_upload():

    form_selections = [
    request.forms.get('selection_1') == 'on',
    request.forms.get('selection_2') == 'on',
    request.forms.get('selection_3') == 'on',
    request.forms.get('selection_4') == 'on' ]

    file_name = request.forms.get('file_name')
    file_location = "downloads/{file_name}".format(file_name=file_name)

    # really want to send this to something else
    #  then it puts it in a database and we can query it later
    # Reall create a new process,and modules are multithreaded

    ouput = []

    if form_selections[0]:
        ouput.append(filetype_module(file_location))
    else:
        ouput.append("NA")

    if form_selections[1]:
        ouput.append(md5_module(file_location))
    else:
        ouput.append("NA")

    if form_selections[2]:
        ouput.append(sha1_module(file_location))
    else:
        ouput.append("NA")


    # return "File successfully saved to '{0}'.".format(save_path)
    return template('output', file_type=ouput[0], sha1=ouput[1], md5=ouput[2])

# run it
run(host='localhost', port=8080)
