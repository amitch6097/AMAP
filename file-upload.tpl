%include header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">File Input Page</h3>
  </div>
  <div class="row">
    <div class="col-12 grid-margin">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">File Input</h4>
          <form action="/upload" method="post" enctype="multipart/form-data">
            Select a file: <input type="file" name="upload" />
            <input type="submit" value="Start upload" />
          </form>
        </div>
      </div>
    </div>

  </div>
</div>


%include footer
