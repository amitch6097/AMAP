%include header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">File Output Page</h3>
  </div>

  <form action="/file-rerun" method="post" enctype="multipart/form-data">
    <input type="hidden" name="id" value="{{file_obj['_id']}}">

  <div class="row">
    <div class="col-12 grid-margin">
      <div class="card">
        <div class="card-body">
            <h4 class="card-title">{{file_obj['Name']}}</h4>
            <div>
              %for key, value in file_obj.iteritems():
                    <div>
                      <h5 class="font-weight-bold">{{key}}:</h5>
                      <div style="margin-left:20px;">
                      % if isinstance(value, list):

                        % for element in value:
                          <p>{{element}}</p>
                        % end

                      %else:
                        <p>{{value}}</p>
                        %end
                      </div>

                    </div>

              %end
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <div class="form-row align-items-center">
              <!-- <label class="form-check-label">
                <input type="checkbox" class="form-check-input" name="selection_1">
                Match Modules For all Files
              </label> -->
              <div class="col-auto ml-auto">
                <button type="submit" class="btn btn-success">Start New Process</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </form>


  </div>
</div>


%include footer
