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
                    Name
                  </th>
                  <th>
                    Overall Progress
                  </th>
                  <th>
                    ID
                  </th>
                  <th>
                    Start Date
                  </th>
                  <th>
                    Due Date
                  </th>
                </tr>
              </thead>
              <tbody>

                % for index, file_name in enumerate(file_names):
                <tr>
                  <td>
                    {{index + 1}}
                  </td>
                  <td>
                    {{file_name}}
                  </td>
                  <td>
                    <div class="progress">
                      <div class="progress-bar bg-gradient-success" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                  </td>
                  <td>
                    ST-3
                  </td>
                  <td>
                    May 10, 2015
                  </td>
                  <td>
                    May 15, 2015
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
