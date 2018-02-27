%include layouts/header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">File Output Page</h3>
  </div>
  <div class="row">
    <div class="col-12 grid-margin">
      <div class="card">
        <div class="card-body">
            <h4 class="card-title">{{file_obj['Name']}}</h4>
            <div>
                  <p>SHA256: {{file_obj['SHA256']}}</p>
                  <p>MD5: {{file_obj['MD5']}}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>


%include layouts/footer
