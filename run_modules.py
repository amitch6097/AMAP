import os
import subprocess
import sys
# import our modules
sys.path.insert(0, 'modules/')

from static_type import filetype_module
from static_hashes import sha1_module, md5_module



def processData(data):
    retList = []
    aStr = ""
    for c in data:
        if c == "\n":
            retList.append(aStr)
            aStr = ""
        else:
            aStr += c

    return retList

def run_modules(array_of_process_objs, debug):
    # for process_obj in array_of_process_objs:
    process = array_of_process_objs[0]
    cwd = os.getcwd()

    output_obj = {"Name":process.file.filename, "location":process.file.path}


    for module in process.modules:

        location_of_module = '{0}/modules/{1}/{1}.py'.format(cwd, module)

         # PRINT OUTPUT TO CONSOLE
        if debug==True:
            p = subprocess.Popen(['python', location_of_module, process.process.file.path])

        else:
            p = subprocess.Popen(['python', location_of_module, process.file.path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdoutdata, stderrdata = p.communicate()

            output = processData(stdoutdata)
            output_obj[module] = output

    return output_obj


def modules(form_selections,file_location):
    # really want to send this to something else
    #  then it puts it in a database and we can query it later
    # Reall create a new process,and modules are multithreaded

    output = []
    output_obj = {}

    if form_selections[0]:
        output.append("File Type: "+filetype_module(file_location))
        output_obj["filetype"] = filetype_module(file_location)
    else:
        output.append("")

    if form_selections[1]:
        output.append("md5: "+md5_module(file_location))
        output_obj["md5"] = md5_module(file_location)

    else:
        output.append("")

    if form_selections[2]:
        output.append("sha1: "+sha1_module(file_location))
        output_obj["sha1"] = sha1_module(file_location)

    else:
        output.append("")

    cwd = os.getcwd()

    #This stays the same
    locationOfDecoder = cwd + '/RatDecoders/ratdecoder.py'

    #Your path to the malware sample
    #locationOfMalware = cwd + '/RatDecoders/DarkComet.exe'

    #subprocess.call(['python', locationOfDecoder, file_location])

    p = subprocess.Popen(['python', locationOfDecoder, file_location], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate()
    #return processData(stdoutdata)

    # execStr = "python2 " + cwd + "/../RatDecoders/ratdecoder.py " + cwd + "/../RatDe
    # os.system(execStr)

    outData = processData(stdoutdata)
    output_obj["RAT"] = "<p>{0}</p>".format("</p><p>".join(outData).encode('ascii', 'xmlcharrefreplace'))


    # return "File successfully saved to '{0}'.".format(save_path)
    output += outData
    return output, output_obj
