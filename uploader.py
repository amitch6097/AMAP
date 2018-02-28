import os

class Malware:
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path
        self.id = -1
        self.runs = 0

    def edit_id(self, id):
        self.id = id

    def to_database_file(self):
        return {
            'Name'      :self.filename,
            'location'  :self.path,
            'runs'      :self.runs
        }

class MalwareUploader:

    def __init__(self, path):
        self.dir = "downloads"
        self.upload_dir = "{0}/{1}".format(path, self.dir)
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

        self.state = "upload"
        self.current_uploads = []
    def reset(self):
        self.state = "upload"
        self.current_uploads = []

    def has_uploads(self):
        if(self.state != "upload"):
            return True

    def get_current_upload_filenames(self):
        file_name_array = [f.filename for f in self.current_uploads]
        return file_name_array

    def add_preloaded(self, db_file, Database):
        self.state = "modules"
        malware = Malware(db_file['Name'], db_file['location'])
        self.current_uploads.append(malware)
        malware.edit_id(db_file['_id'])
        malware.runs = db_file['runs']
        # Database.db_insert_malware_obj(malware)


    #TODO handle uploads with same names
    def upload(self, file_uploads, Database):
        self.state = "modules"
        for upload in file_uploads:

            # How to not allow file types
            # name, ext = os.path.splitext(upload.filename)
            # if ext not in ('.not', '.allowed', '.example'):
            #     return "File extension not allowed."

            file_path = "{path}/{file}".format(path=self.upload_dir, file=upload.filename)
            upload.save(file_path, overwrite=True)

            malware = Malware(upload.filename, file_path)
            self.current_uploads.append(malware)
            Database.db_insert_malware_obj(malware)
