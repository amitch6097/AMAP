%include header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">Modules</h3>
  </div>
  <div class="form-group">
    <form action="/process" method="post" enctype="multipart/form-data">
      <input type="hidden" name="file_name" value={{file}}>
      <div class="form-check form-check-flat">
        <label class="form-check-label">
          <input type="checkbox" class="form-check-input" name="selection_1">
          Match Modules For all Files
        </label>
      </div>
    </form>
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
                  <input type="checkbox" class="form-check-input" name="file_type" checked>
                  File Type
                </label>
              </div>
              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" class="form-check-input" name="md5" checked>
                  MD5
                </label>
              </div>
              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" class="form-check-input" name="sha1" checked>
                  SHA1
                </label>
              </div>
              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" class="form-check-input" name="sha256" checked>
                  SHA256
                </label>
              </div>
              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" class="form-check-input" name="entropy" checked>
                  Entropy
                </label>
              </div>
              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" class="form-check-input" name="decoder" checked>
                  Decoder
                </label>
              </div>
              <div class="form-check form-check-flat">
                <label class="form-check-label">
                  <input type="checkbox" class="form-check-input" name="netdata" checked>
                  NETDATA
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
