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
</style>

  <div class="content-wrapper">
    <div class="row">
      <h3 class="text-info">New Module</h3>
    </div>
    <form id="code-form" action="/module-create" class="h-75" method="post" enctype="multipart/form-data">
      <input type="hidden" id="code-text-input"name="code-text-input">


      <div class="h-100 col-12 stretch-card grid-margin">
        <div class="card h-100 " style="padding-bottom:40px;">
          <div class="card-body h-100">
          <div class="form-row">
            <div class="form-group text-center " style="margin:0 auto;">
              <div class="input-group col-xs-12">
                <input type="text" id="module-name" name="module-name" value="{{module_name}}" class="form-control file-upload-info" placeholder="File Name" style="width:250px">
                <span class="input-group-btn">
                  <button class="file-upload-browse btn btn-info" type="button" onclick="saveFile(event)">Upload</button>
                </span>
            </div>
          </div>
          </div>
          <div class="row h-100" style="padding-bottom:20px">
          <div id="editor" class="h-100">
%for line in file_contents:
{{line}}
%end
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
  function saveFile(event) {
      event.preventDefault();
      var name = document.getElementById("module-name").value.replace(" ", "")
      if(!name || name === '')
      {
        alert("Please Name the Module")
        return false
      } else {
        var code  = editor.getValue()
        document.getElementById("code-text-input").value = code;
        document.getElementById("code-form").submit();
      }

  }
  </script>


%include footer
