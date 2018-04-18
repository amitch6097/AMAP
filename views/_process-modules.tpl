
<div class="col-6" style="margin: 0 auto; margin-top: 200px;">

  <div class="card" style="border-radius:10px; padding:10px;">

  <form action="/_process" method="post" name="submit-processes-form" enctype="multipart/form-data" style="height: 500px;overflow: scroll;border:1px solid #e8e8e8">



    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title">Module Selector</h2>
            <div class="form-row align-items-center">
              <label class="form-check-label">
                <input type="checkbox" id="match-checkbox" class="form-check-input" onclick="matchIt()" name="selection_1">
                Match All Modules to First Module
              </label>
              <div class="col-auto ml-auto">
                <button type="submit" class="btn btn-info">Submit</button>
              </div>
            </div>
            <div class="form-row align-items-center">
              <button onclick="SelectAll(event)" class="btn btn-success" style="margin-right:20px;">Select All Modules</button>
              <button onclick="DeselectAll(event)" class="btn btn-secondary">Deselect All Modules</button>
            </div>
          </div>
        </div>
      </div>
    </div>

  <input type="hidden" id="file-count" value="{{len(file_names)}}">
 % for i, file in enumerate(file_names):

  <div class="row" style="text-align:left; margin:0px; margin-left:20px">
    <div class="form-group">
    <h4>{{file}}</h4>
    <input type="hidden" name="n1" value="thisvalue">
        % for index, option in enumerate(module_options):
        % name = "{0}_{1}".format(file, index)
        <div class="form-check" style="">
          <input type="checkbox" style="margin-left:0px;" id="form-check-input-module" class="form-check-input module {{i}}" onclick="checkMatch()" name='{{name}}' checked>
          <label class="form-check-label">
            {{option}}
          </label>
        </div>
        % end
      </div>
    </div>
  % end
  </form>
</div>
</div>
<script type="text/javascript">

    $('form[name=submit-processes-form]').submit(function(e){
        e.preventDefault();
        $.ajax({
            type: 'POST',
            cache: false,
            url: './_process',
            data: 'id=header_contact_send&'+$(this).serialize(),
            success: function(msg) {
                // $("#file-input-section").html(msg);
                document.getElementById("overlay").style.display = "none";
                document.getElementById("module-upload-submit").value = ""

                getProcesses()

                return false
            }
        });
        return false;
    });

    var match = false;

    function matchIt() {
      match = document.getElementById("match-checkbox").checked;
      checkMatch();
    }

    function checkMatch() {
      if(!match){
        return true;
      }
      var elementsFirstRow = document.getElementsByClassName("form-check-input module 0");
      var def = [];

      for(var i=0; i<elementsFirstRow.length; i++) {
          def.push(elementsFirstRow[i].checked)
      }
      var fileCount = parseInt(document.getElementById("file-count").value);

      for(var k=0; k<fileCount; k++) {
        var elements = document.getElementsByClassName("form-check-input module "+k);

        for(var j=0; j<elements.length; j++) {
            elements[j].checked = def[j];
        }
      }
    }

    function SelectAll(event) {
      event.preventDefault();
      var elements = document.getElementsByClassName("form-check-input module");
      for(var i=0; i<elements.length; i++) {
          elements[i].checked = true;
      }
    }
    function DeselectAll(event) {
      event.preventDefault();
      var elements = document.getElementsByClassName("form-check-input module");
      for(var i=0; i<elements.length; i++) {
          elements[i].checked = false;
      }
    }
  </script>
