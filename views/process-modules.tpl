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
                <input type="checkbox" class="form-check-input" name="selection_1">
                Match Modules For all Files
              </label>
              <div class="col-auto ml-auto">
                <button type="submit" class="btn btn-success">Submit</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

 % for file in file_names:

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
                  <input type="checkbox" class="form-check-input" name='{{name}}' checked>
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

%include footer
