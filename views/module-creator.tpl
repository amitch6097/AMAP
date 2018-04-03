%include header
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="node_modules/jquery/dist/jquery.min.js"></script>

<style type="text/css" media="screen">
#editor {
    width: 100%;
    height: 100%;
    border: 2px solid #e8e8e8;
    margin-top:20px;
}
.form-row align-items-center {
  padding:10;
}
</style>

  <div class="content-wrapper">
    <div class="row">
      <h3 class="text-info">New Module</h3>
    </div>
    <form id="code-form" action="/module-create" class="h-75" method="post" enctype="multipart/form-data">
      <input type="hidden" id="code-text-input"name="code-text-input">


      <div class="h-100 col-12 stretch-card grid-margin">
        <div class="card  h-100 ">
          <div class="card-body h-100">
          <div class="form-row align-items-center">
            <input type="button" class="btn btn-warning" value="Reset" />
            <h1>Name: </h1>
            <input type="text" name="module-name"/>

            <div class="col-auto ml-auto">
              <input type="submit" class="btn btn-success" value="Submit" onclick="saveFile()"/>
            </div>
          </div>
          <div class="row h-100" style="padding-bottom:20px">
          <div id="editor" class="h-100">import os

import hashlib
from optparse import OptionParser


__description__ = 'SHA256'
__author__ = 'Andrew Mitchell'
__version__ = '1.0'
__date__ = '2016/04'

def sha1_module(filename):
    openedFile = open(filename)
    readFile = openedFile.read()
    # print filename

    sha1Hash = hashlib.sha1(readFile)
    sha1Hashed = sha1Hash.hexdigest()

    print sha1Hashed

if __name__ == "__main__":
        parser = OptionParser(usage='usage: %prog file / dir\n' + __description__, version='%prog ' + __version__)
        (options, args) = parser.parse_args()
        is_file = os.path.isfile(args[0])
        if is_file:
            sha1_module(args[0])

          </div>

          <script src="//cdnjs.cloudflare.com/ajax/libs/ace/1.3.3/ace.js"></script>
          <script src="//cdnjs.cloudflare.com/ajax/libs/ace/1.3.3/mode-python.js" type="text/javascript" charset="utf-8"></script>
          <script>
              var editor = ace.edit("editor");
              editor.setTheme("ace/theme/chrome");
              editor.session.setMode("ace/mode/python");
            </script>
          </div>
        </div>
      </div>
    </div>
  </form>

  </div>

  <script>
  function saveFile() {
      // var code = document.getElementById("editor").innerHTML;
      var code  = editor.getValue()
      document.getElementById("code-text-input").value = code;
      document.getElementById("code-form").submit();
  }
  </script>


%include footer
