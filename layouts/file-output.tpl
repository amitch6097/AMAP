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
  </div>
</div>


%include layouts/footer
