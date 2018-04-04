%include header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">Modules</h3>
  </div>
  <form action="/process" method="post" enctype="multipart/form-data">



    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
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

  <div class="row">
    <div class="col-12 grid-margin">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">{{file}}</h4>
          <input type="hidden" name="n1" value="thisvalue">

          <div class="form-group">
              % for index, option in enumerate(module_options):
              % name = "{0}_{1}".format(file, index)

              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" id="form-check-input-module" class="form-check-input module {{i}}" onclick="checkMatch()" name='{{name}}' checked>
                  {{option}}
                </label>
              </div>
              % end
            </div>

          </div>
        </div>
      </div>
    </div>

  % end

  </form>
</div>
<script>
var match = false;

function matchIt() {
  match = document.getElementById("match-checkbox").checked;
  checkMatch();
}
</script>
<script>

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
</script>
<script>
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
%include footer
