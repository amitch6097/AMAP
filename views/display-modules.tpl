%include header


<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">My Modules</h3>
  </div>

  <!--TODO not output but button leading to page -->
  %for obj in modules:

    <form action="/delete-module" method="post" enctype="multipart/form-data">
    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <div class="form-row align-items-center">
              <label class="form-check-label">
                  <h4>{{obj}}</h4>
              </label>
              <div class="col-auto ml-auto">
                <button type="submit" class="btn btn-success btn-fw" style="min-width: 12px; margin-right:20px">Update</button>
                <button type="submit" class="btn btn-danger btn-fw" style="min-width: 12px;">Delete</button>
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



%include footer
