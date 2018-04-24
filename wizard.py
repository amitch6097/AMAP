#CLASS to define the setup wizard
class Wizard:

    #   module_list   - list
    #   running     - boolean
    #   time        -val
    #   numfiles    -integer
    def __init__(self):
        self.module_list = []
        self.running = False
        self.time = -1
        self.numFiles = -1
    #   resets the number of files and time
    def resetConfig(self):
        self.time = -1
        self.numFiles = -1
    #   adds a new module to the list
    #   PARAM module the module name to append
    def addModule(self, module):
        self.module_list.append(module)
    #   returns the list of modules used by the wizard
    def getModules(self):
        return self.module_list
    #   returns whether the wizard is currrently running 
    def isRunning(self):
        return self.running
    #   sets the wizard to start running
    def startRunning(self):
        self.running = True
    #   stops the wizard's running and resets the parameters
    def stopRunning(self):
        self.resetConfig()
        self.running = False
    #   sets whethere each available module will be used in the next run of the wizard
    #   PARAM forms the forms where the values of the checkboxes are retrieved from
    #   PARAM all_modules list of all the modules that are being set for the wizard
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
    #   sets the configuration of the wizard, the number of files and the time between each pull
    #   PARAM forms the forms that contain the text boxes where the configuration values are entered
    def setConfig(self, forms):
        t = forms.get("files-to-select")
        n = forms.get("time-between-select")
        if n == "" or t == "":
            self.time = 10
            self.numFiles = 1
        else:
            self.numFiles = int(forms.get("files-to-select"))
            self.time = int(forms.get("time-between-select"))
    #   getter for the time between each pull
    #   RETURNS time the time between each pull of files
    def getTimeInterval(self):
        return self.time
    #   getter for the number of files to pull at each interval
    #   RETURNS numFiles the number of files that get pull in each batch
    def getFileGrabInterval(self):
        return self.numFiles
    #   prints the configuration, numFiles and time
    def printConfig(self):
        print "****** PRINT CONFIG ******"
        print self.time
        print self.numFiles
    #   getter for the module_list
    #   RETURNS module_list the list of modules available to the wizard
    def getModules(self):
        return self.module_list
