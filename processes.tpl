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
                  </th>
                </tr>
              </thead>
              <tbody>

                % for index, file_name in enumerate(file_names):
                % percent = percent_done[index]

                <a href={{file_name}}>
                  <tr>
                    <td>
                      {{index + 1}}
                    </td>
                    <td>
                      {{file_name}}
                    </td>
                    <td>
                      <div class="progress">
                        <div class="progress-bar bg-info" role="progressbar" style="width: {{percent}}%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </td>
                    <td>
                      ST-3
                    </td>
                    <td>
                      {{1}}
                    </td>
                    <td>
                      <form action="/file_view" method="post" enctype="multipart/form-data">
                          <button type="submit" class="btn btn-info btn-fw">View</button>
                      </form>
                    </td>
                  </tr>
                </a>
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
