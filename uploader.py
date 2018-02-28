import os

class Malware:
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path

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


    #TODO handle uploads with same names
    def upload(self, file_uploads):
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
