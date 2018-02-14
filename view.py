
import sys
#trouble adding path so ...
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/")

import os
from bottle import static_file, run, template, get, redirect, request, route

@route('/')
def default():  return redirect('/index.html')

@route('/upload', method='POST')
def do_upload():
    current_dir_path = os.path.dirname(os.path.realpath(__file__))

    # grab uploaded file from form
    upload = request.files.get('upload')

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

    return "File successfully saved to '{0}'.".format(save_path)

@route('/<name>')
def index(name):
    return static_file(name, root="static/")

# # Static Routes
@get('/<filename:path>')
def static(filename):
    return static_file(filename, root='static/')

# run it
run(host='localhost', port=8080)
