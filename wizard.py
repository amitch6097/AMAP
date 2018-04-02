#CLASS to define the setup wizard
class Wizard:

    #   module_list   - list
    #   isRunning     - boolean
    def __init__(self):
        self.module_list = []
        self.running = False
        self.time = -1
        self.numFiles = -1

    def resetConfig(self):
        self.time = -1
        self.numFiles = -1

    def addModule(self, module):
        self.module_list.append(module)

    def getModules(self):
        return self.module_list

    def isRunning(self):
        return self.running

    def startRunning(self):
        self.running = True

    def stopRunning(self):
        self.resetConfig()
        self.running = False

    def setModules(self, forms, all_modules):
        mList = []
        # loop through all of the possible modules
        for index, module in enumerate(all_modules):

            # the name of the check box input is the form
            # 'FILENAME_INDEX-OF-MODULE'
            name = "{0}".format(index)

            #grab the checkbox value
            checkbox = forms.get(name)

            #if it is on
            if (checkbox == 'on'):
                #add the string name to the process's modules
                mList.append(module)
        self.module_list = mList
        print self.module_list

    def setConfig(self, forms):
        t = forms.get("files-to-select")
        n = forms.get("time-between-select")
        if n == "" or t == "":
            self.time = 10
            self.numFiles = 1
            return
        else:
            self.time = int(forms.get("files-to-select"))
            self.numFiles = int(forms.get("time-between-select"))

    def getTimeInterval(self):
        return self.time

    def getFileGrabInterval(self):
        return self.numFiles

    def printConfig(self):
        print "****** PRINT CONFIG ******"
        print self.time
        print self.numFiles

    def getModules(self):
        return self.module_list





