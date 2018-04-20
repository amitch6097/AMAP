
  <div class="row">
    <div class="col-md-12 grid-margin stretch-card">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">Analysis Status</h4>
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>
                    #
                  </th>
                  <th>
                    File Name
                  </th>
                  <th>
                    Run #
                  </th>
                  <th>
                    Start Time
                  </th>
                  <!-- <th>
                    Overall Progress
                  </th> -->
                  <th>
                    End Time
                  </th>
                  <th>
                  </th>
                  <th>
                  </th>
                </tr>
              </thead>
              <tbody>


                %index = 0
                % for process in processes:
                  %index+=1

                  <tr>
                    <td>
                      {{index}}
                    </td>
                    <td>
                      {{process.file_name}}
                    </td>
                    <td>
                      {{process.run_number}}
                    </td>
                    <td>
                      {{process.start_time}}
                    </td>
                    <!-- <td>
                      <div class="progress">
                        <div class="progress-bar bg-info" role="progressbar" style="width: {{process.percent_done}}%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </td> -->
                    <td>
                      {{process.end_time}}
                    </td>
                    <td>

                      <button class="btn btn-primary" onclick="showModules(event, '{{index}}')" type="button" data-toggle="collapse" data-target="#collapseExample{{index}}" aria-expanded="false" aria-controls="collapseExample">
                        Display Modules
                      </button>
                    </td>

                    <td>
                      <form id="{{index}}" enctype="multipart/form-data">
                          <button type="button" onclick="fileView(event, '{{index}}')" class="btn btn-info btn-fw" style="min-width: 12px;">View</button>
                          <input type="hidden" name="filename" id="filename" value={{process.file_name}}>
                      </form>
                    </td>
                  </tr>
                  <tr style="display:none; text-align: left;" id="{{index}}row">
                    <td>
                    </td>
                    <td style="text-align: left;">

                      <!-- <div class="collapse" id="collapseExample"> -->
                        %for module in process.modules:
                          %if process.modules[module] == True:
                          <p style="display:inline-flex;">
                          <i class="mdi mdi-circle mr-2 text-primary"></i>
                            {{module}}
                          </p>
                          %else:
                          <p style="display:inline-flex;">
                            <i class="mdi mdi-circle mr-2 text-danger"></i>
                            {{module}}
                          </p>
                          %end
                        %end
                      <!-- </div> -->
                    </td>
                  </tr>
                 % end

              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>


<script>



</script>
