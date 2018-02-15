%include header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">Modules</h3>
  </div>

 % for file in file_names:
  <div class="row">
    <div class="col-12 grid-margin">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">{{file}}</h4>

          <div class="form-group">
            <form action="/process" method="post" enctype="multipart/form-data">
              <input type="hidden" name="file_name" value={{file}}>
              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" class="form-check-input" name="selection_1">
                  File Type
                </label>
              </div>
              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" class="form-check-input" name="selection_2">
                  md5
                </label>
              </div>
              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" class="form-check-input" name="selection_3">
                  sha1
                </label>
              </div>
              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" class="form-check-input" name="selection_4">
                  Dynamic Analysis 2
                </label>
              </div>
              <button type="submit" class="btn btn-success mr-2">Submit</button>
            </form>
          </div>

        </div>
      </div>
    </div>
  </div>
  % end
</div>


%include footer
