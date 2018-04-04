%include header


<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">My Modules</h3>
  </div>
  <form id="my-modules-form_" class="pagination-centered" method="post" style="text-align: center;" enctype="multipart/form-data">
    <button type="submit" class="btn btn-success btn-fw" style="min-width: 12px; margin:30px; padding:15px 60px" onclick="fileEdit('')">Create New Module</button>
  </form>

  <!--TODO not output but button leading to page -->
  %for obj in modules:
  <form id="my-modules-form_{{obj}}" method="post" enctype="multipart/form-data">
    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <div class="form-row align-items-center">
              <label class="form-check-label">
                  <h4>{{obj}}</h4>
              </label>
              <div class="col-auto ml-auto">
                <button type="submit" class="btn btn-success btn-fw" style="min-width: 12px; margin-right:20px" onclick="fileEdit('{{obj}}')">Update</button>
                <button type="submit" class="btn btn-danger btn-fw" style="min-width: 12px;" onclick="fileDelete('{{obj}}')">Delete</button>
                <input type="hidden" name="module-name" value="{{obj}}">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
  %end
</div>

<script>
function fileEdit(obj) {
  document.getElementById("my-modules-form_"+obj).action = "my-modules-creator";
  document.getElementById("my-modules-form_"+obj).submit();
}
function fileDelete(obj) {
  console.log("DELTE")
  document.getElementById("my-modules-form_"+obj).action = "delete-module";
  document.getElementById("my-modules-form_"+obj).submit();
}
</script>




%include footer
