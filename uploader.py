import os
import time
import hashlib


#CLASS to define a single file or malware upload
class Malware:

    #   filename   - string
    #   path       - string path the to file on system
    def __init__(self, filename, path, hashes):
        self.filename = filename
        self.path = path
        self.hashes = hashes

        self.id = -1
        self.runs = 0
        self.time = time.time()

    def edit_id(self, id):
        self.id = id

    def to_database_file(self):
        return {
            'Name'      :self.filename,
            'location'  :self.path,
            'runs'      :self.runs,
            'time'      :self.time,
            'hashes'    :self.hashes
        }

#CLASS to upload malware and get current uploaded files
class MalwareUploader:

    # takes the current path of view.py
    # makes downloads folder if necessary
    def __init__(self, path):
        self.dir = "downloads"
        self.upload_dir = "{0}/{1}".format(path, self.dir)
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

        self.hashed_dir = "{0}/{1}".format(path, "hashed")
        if not os.path.exists(self.hashed_dir):
            os.makedirs(self.hashed_dir)

        #two states "upload" and "module"
        #defines wether or not we are uploading a file
        # or setting the modules to run on a file
        self.state = "upload"
        self.current_uploads = []

    #reset state to uploading and clear uploads
    def reset(self):
        self.state = "upload"
        self.current_uploads = []

    # if we have files that are uploaded
    def has_uploads(self):
        if(self.state != "upload"):
            return True

    # get the current uploaded files in an array
    def get_current_upload_filenames(self):
        file_name_array = [f.filename for f in self.current_uploads]
        return file_name_array

    # ran when we are running moudles on a file that is
    # already in our database -- we don't need to upload it
    #
    #   db_file   - the database object of the file
    #   Database  - our global database obj
    def add_preloaded(self, db_file, Database):

        self.state = "modules"

        #create a Malware object from the database file
        malware = Malware(db_file['Name'], db_file['location'])

        self.current_uploads.append(malware)

        malware.edit_id(db_file['_id'])

        malware.runs = db_file['runs']
        # Database.db_insert_malware_obj(malware)

    def get_hashes_and_move_file(self, file_path, Database, filename):
        opened_file = open(file_path)
        read_file = opened_file.read()

        sha1= hashlib.sha1(read_file).hexdigest()
        sha256 = hashlib.sha256(read_file).hexdigest()
        md5 = hashlib.md5(read_file).hexdigest()
        hashes = {"sha1":sha1, "sha256":sha256, "md5":md5}

        name = "{0}_{1}".format(sha1, md5)
        new_path = os.path.join(self.hashed_dir, name)

        malware = Malware(filename, new_path, hashes)

        if os.path.isfile(new_path):
            Database.db_add_name_to_malware(new_path, filename, malware)
        else:
            os.rename(file_path, new_path)
            Database.db_insert_malware_obj(malware)

        #add it to current uploads for later processing
        self.current_uploads.append(malware)



    #TODO handle uploads with same names
    # Uploads files to the downloads folder
    #
    #   file_uploads   - files from a form post action, array
    #   Database       - our global database object
    def upload(self, file_uploads, Database):
        self.state = "modules"

        for upload in file_uploads:
            # How to not allow file types
            # name, ext = os.path.splitext(upload.filename)
            # if ext not in ('.not', '.allowed', '.example'):
            #     return "File extension not allowed."

            #set the file path and save it
            file_path = "{path}/{file}".format(path=self.upload_dir, file=upload.filename)
            upload.save(file_path, overwrite=True)

            self.get_hashes_and_move_file(file_path, Database, upload.filename)
