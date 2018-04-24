
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="node_modules/jquery/dist/jquery.min.js"></script>

<style type="text/css" media="screen">
#editor {
    width: 100%;
    height: 400%;
    border: 2px solid #e8e8e8;
    margin-top:20px;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
}
</style>

  <div class="content-wrapper" style="margin-top:100px">
    <div class="card">
      <div class="card-body">

      <h4 class="card-title" style"margin:10px;">Module Editor</h4>
    <form id="code-form" action="/module-create" method="post" onSubmit="saveFile(event)" enctype="multipart/form-data">
      <input type="hidden" id="code-text-input"name="code-text-input">
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="form-group text-center " style="margin:0 auto;">
                <div class="input-group col-xs-12">
                  <input type="text" id="module-name" name="module-name" value="{{module_name}}" class="form-control file-upload-info"  placeholder="File Name" style="width:250px">
                  <span class="input-group-btn">
                    <button class="file-upload-browse btn btn-info" type="button" onclick="saveFile(event)">Save</button>
                  </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row" style="height:500px;">
      <div class="col-12 stretch-card grid-margin" style="height:500px;">
        <div class="card" style="height:500px;">
          <div class="card-body" style="height:500px;">
            <div id="editor" style="height:500px;">
  %for line in file_contents:
  {{line}}
  %end
            </div>
        </div>
      </div>
    </div>
  </div>

  </form>
</div>
</div>
  </div>

  <script>
  var editor = ace.edit("editor");
  editor.setTheme("ace/theme/chrome");
  editor.session.setMode("ace/mode/python");
  </script>
