
  <form id="my-modules-form_" method="post" enctype="multipart/form-data">
    <button type="submit" class="btn btn-success btn-fw" style="min-width: 12px; margin:30px; padding:15px 60px" onclick="createNew(event)">Create New Module</button>
  </form>

  <!--TODO not output but button leading to page -->
  %for obj in modules:
  <form id="my-modules-form_{{obj}}" method="post" name="current-module-form" enctype="multipart/form-data">
    <div class="row">
      <div class="col-12 grid-margin" style="margin-bottom: 10px;">
        <div class="card">
          <div class="card-body" style="padding:10px; border: 1px solid #c0c0c0; border-width: 1px 0px 0px 0px; margin-left:20px;margin-right:20px">
            <div class="form-row align-items-center">
              <label class="form-check-label">
                  <h4>{{obj}}</h4>
              </label>
              <div class="col-auto ml-auto">
                <button type="button" class="btn btn-success btn-fw" style="min-width: 12px; margin-right:20px" onclick="fileEdit('{{obj}}')">Edit</button>
                <button type="button" class="btn btn-danger btn-fw" style="min-width: 12px;" onclick="fileDelete('{{obj}}')">Delete</button>
                <input type="hidden" name="module-name" value="{{obj}}">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
  %end

  <script src="//cdnjs.cloudflare.com/ajax/libs/ace/1.3.3/ace.js"></script>
  <script src="//cdnjs.cloudflare.com/ajax/libs/ace/1.3.3/mode-python.js" type="text/javascript" charset="utf-8"></script>
<script>
function createNew(event) {
  event.preventDefault()
  document.getElementById("my-modules-form_").action = "_my-modules-creator";
  $form = $("#my-modules-form_");

  $.ajax({
      type: 'POST',
      cache: false,
      url:"_my-modules-creator",
      data: 'id=header_contact_send&'+$form.serialize(),
      success: function(msg) {
        $( "#module-creator-section" ).html(msg);
        $( "#module-creator-section" ).css("display", "block");
        $( "#module-page" ).css("display", "none");
        return false
      }
  });
  return false
}

function fileEdit(obj) {
  document.getElementById("my-modules-form_"+obj).action = "_my-modules-creator";
  $form = $("#my-modules-form_"+obj);

  $.ajax({
      type: 'POST',
      cache: false,
      url:"_my-modules-creator",
      data: 'id=header_contact_send&'+$form.serialize(),
      success: function(msg) {
        $( "#module-creator-section" ).html(msg);
        $( "#module-creator-section" ).css("display", "block");
        // $( "#module-page" ).css("display", "none");

        return false
      }
  });
  return false
}
function fileDelete(obj) {
  document.getElementById("my-modules-form_"+obj).action = "_delete-module";
  $form = $("#my-modules-form_"+obj);
  $.ajax({
      type: 'POST',
      cache: false,
      url:"_delete-module",
      data: 'id=header_contact_send&'+$form.serialize(),
      success: function(msg) {
        getModules();
        return false
      }
  });
  return false
}

function saveFile(event) {
    event.preventDefault();
    var name = document.getElementById("module-name").value.replace(" ", "")
    var code  = editor.getValue()
    document.getElementById("code-text-input").value = code;
    if(!name || name === '')
    {
      alert("Please Name the Module")
      return false
    } else {
      // document.getElementById("code-form").submit();
      $form = $("#code-form");
      $.ajax({
          type: 'POST',
          cache: false,
          url:"module-create",
          data: 'id=header_contact_send&'+$form.serialize(),
          success: function(msg) {
            getModules();
            $( "#module-creator-section" ).css("display", "none");
            $( "#module-page" ).css("display", "block");
            return false
          }
      });
    }

}
</script>
