%include header


<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">Search</h3>
  </div>

  <!--TODO not output but button leading to page -->
  %if len(search_output) == 0:
  <div class="row">
    <div class="col-12 grid-margin">
      <div class="card">
        <div class="card-body">
            <h4 class="card-title">No Matching Files</h4>
          </div>
        </div>
      </div>
    </div>
  %else:
  %for obj in search_output:

    <!-- <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title">{{obj['Name']}}</h4>
            <form action="/file_view" method="post" enctype="multipart/form-data">
                <button type="submit" class="btn btn-info btn-fw" style="min-width: 12px;">View</button>
                <input type="hidden" name="filename" value={{obj['Name']}}>
            </form>
          </div>
        </div>
      </div>
    </div> -->
    <form action="/file_view" method="post" enctype="multipart/form-data">
    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <div class="form-row align-items-center">
              <label class="form-check-label">
                  <h4>{{obj['Name']}}</h4>
              </label>
              <div class="col-auto ml-auto">
                <button type="submit" class="btn btn-info btn-fw" style="min-width: 12px;">View</button>
                <input type="hidden" name="filename" value={{obj['Name']}}>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>

  %end
  %end

</div>



%include footer
