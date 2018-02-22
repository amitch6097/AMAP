# coding=utf-8
import sys
#trouble adding path so ...
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/")

import os
import run_modules
from bottle import static_file, run, template, get, redirect, request, route, template
import json


@route('/')
def default():
    # return template('dashboard')
    return template('layouts/dashboard')

    # return redirect('/index.html')


@route('/processes')
def load_processes():
    file_names = ['b3d9cabf3ecb22dbccbd0f13f95313e5ab95be94aec879e6edfaaf534d7f3799', 'dff02aca142d4fcffe7721b9c7cb5d7d4ef4965d11e77328d290aaf2eac8d4dd', 'dcf789f34aabe7ba4c34bbce09bfdd6ac6a2efde9f664ec0eab16fd0e37bef0d', '2e112bbf5fa0afaf225eb2441b245539cd73f52fb473a6b749490d4749f7d105', '9ac3accd466a70884091364b5d2e13534cfa78153b25f51fe477d6bfcc6f9abe']
    md5s = ['eb684b584704e2fb599d6eaf883c1ae5', '4871e4752bd67662ac9435d84014391d', '3501fa1f022cb8ad97276d55c97377b5', '9490fe6870d1273dda8c957cf1b81907', '68b329da9893e34099c7d8ad5cb9c940']
    start_time = ['18-1-27 1:54:24', '18-2-2 1:59:32', '18-2-3 5:52:45', '18-2-3 6:00:23', '18-2-5 12:32:02']


    percent_done = [25, 60, 80, 10, 100]
    return template('layouts/processes', file_names=file_names, percent_done=percent_done, md5s=md5s, start_time=start_time)

@route('/file_view', method='POST')
def load_file():
    file_type="PDF"
    md5="oifmeswmfpmgdmskgdsmn"
    sha1="0f9dsifmdsfmdsfijf0e9jfefefe"
    return template('layouts/output', file_type=file_type, sha1=sha1, md5=md5)

@route('/<name>')
def index(name):
    return template("layouts/"+name)

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

    #TODO handle uploads with same names
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
        upload.save(file_path, overwrite=True) #overwrite TRUE might not be good?

        # add to array of names
        uploads_name_array.append(upload.filename)

    info = {'file_names' : uploads_name_array}

    # return "File successfully saved to '{0}'.".format(save_path)
    return template('layouts/process-modules', info)


@route('/mu', method='POST')
def servo_pos():
    uploads = request.files.getall('files[]')
    uploads_name_array = []

    #TODO handle uploads with same names
    for upload in uploads:
        print upload.filename
        uploads_name_array.append(upload.filename)
    return json.dumps(uploads_name_array)



@route('/process', method='POST')
def process_upload():

    form_selections = [
    request.forms.get('file_type') == 'on',
    request.forms.get('md5') == 'on',
    request.forms.get('sha1') == 'on',
    request.forms.get('sha256') == 'on',
	request.forms.get('entropy') == 'on',
	request.forms.get('decoder') == 'on',
	request.forms.get('netdata') == 'on'
	 ]

    file_name = request.forms.get('file_name')
    file_location = "downloads/{file_name}".format(file_name=file_name)
    outData = run_modules.modules(form_selections,file_location)

    return template('layouts/output', ratOutput=outData)


# run it
run(host='localhost', port=8080)
