import os
import time
import hashlib


"""
Defines a Malware sample file object
filename:   name of the sample
path:       path to the file in the system
hashes:     all hashes associated with the file
"""
class Malware:
    def __init__(self, filename, path, hashes):
        self.filename = filename
        self.path = path
        self.hashes = hashes
        self.id = -1
        self.runs = 0
        self.time = time.time()

    def edit_id(self, id):
        self.id = id

    """used when placing object in a mongodb"""
    def to_database_file(self):
        return {
            'Name'      :self.filename,
            'location'  :self.path,
            'runs'      :self.runs,
            'time'      :self.time,
            'hashes'    :self.hashes,
            'sha1'      :self.hashes['sha1'],
            'sha256'    :self.hashes['sha256'],
            'md5'       :self.hashes['md5']
        }

"""
Defines a object which can upload malware to the system
path: string path to the Current working directory
"""
class MalwareUploader:

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

    """reset state to uploading and clear uploads"""
    def reset(self):
        self.state = "upload"
        self.current_uploads = []

    """checks if system has malware uploads to process"""
    def has_uploads(self):
        if(self.state != "upload"):
            return True

    """get the current uploaded files in an array"""
    def get_current_upload_filenames(self):
        file_name_array = [f.filename for f in self.current_uploads]
        return file_name_array

    """
    ran when we are running moudles on a file that is
    already in our database -- we don't need to upload it
    db_file:  the database object of the file
    Database: our global database obj"""
    def add_preloaded(self, db_file, Database):

        self.state = "modules"

        #create a Malware object from the database file
        malware = Malware(db_file['Name'], db_file['location'], db_file["hashes"])
        self.current_uploads.append(malware)
        malware.edit_id(db_file['_id'])
        malware.runs = db_file['runs']

    """retrives the hashes from a file and renames the file based on this"""
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
            if Database.db_add_name_to_malware(new_path, filename, malware) == False:
                os.rename(file_path, new_path)
                Database.db_insert_malware_obj(malware)
        else:
            os.rename(file_path, new_path)
            Database.db_insert_malware_obj(malware)

        #add it to current uploads for later processing
        self.current_uploads.append(malware)



    """Uploads files to the downloads folder
    file_uploads   - files from a form post action, array
    Database       - our global database object
    """
    def upload(self, file_uploads, Database):
        self.state = "modules"

        for upload in file_uploads:
            file_path = "{path}/{file}".format(path=self.upload_dir, file=upload.filename)
            upload.save(file_path, overwrite=True)

            self.get_hashes_and_move_file(file_path, Database, upload.filename)
