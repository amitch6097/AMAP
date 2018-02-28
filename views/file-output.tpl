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
                  % if key != 'RAT':
                    <p>{{key}}: {{value}}</p>
                  % else:
                    <div>{{key}}:
                      % for element in range(len(value)):
                        <p>{{value[element]}}</p>
                      % end
                    </div>
                  % end

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
