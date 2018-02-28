%include header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">Processes</h3>
  </div>


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
                    Start Time
                  </th>
                  <th>
                    Overall Progress
                  </th>
                  <th>
                    End Time
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
                      {{process.file.filename}}
                    </td>
                    <td>
                      {{process.start_time}}
                    </td>
                    <td>
                      <div class="progress">
                        <div class="progress-bar bg-info" role="progressbar" style="width: {{process.percent_done}}%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </td>
                    <td>
                      {{process.end_time}}
                    </td>
                    <td>
                      <form action="/file_view" method="post" enctype="multipart/form-data">
                          <button type="submit" class="btn btn-info btn-fw" style="min-width: 12px;">View</button>
                          <input type="hidden" name="filename" value={{process.file.filename}}>
                      </form>
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


</div>


%include footer
