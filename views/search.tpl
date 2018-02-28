%include header


<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">This is Search</h3>
  </div>

  <!--TODO not output but button leading to page -->
  %for obj in search_output:

    <div class="row">
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
    </div>
  %end

</div>



%include footer
