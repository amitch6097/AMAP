%include layouts/header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">Modules Page</h3>
  </div>
  <div class="row">
    <div class="col-12 grid-margin">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">Upload Modules</h4>
          <form action="/upload-module" method="post" enctype="multipart/form-data">
            % for file in file_names:
              <input type="hidden" name="file_name" value={{file}}>
              <p>{{file}}</p>
              <button type="submit" class="btn btn-success">Submit</button>
            % end
          </form>
        </div>
      </div>
    </div>

  </div>
</div>


%include layouts/footer
