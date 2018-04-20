%include header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">File Output Page</h3>
  </div>

  <form action="/file-rerun" method="post" enctype="multipart/form-data">
    <input type="hidden" name="id" value="{{file_obj['_id']}}">
    <%
      dList = []
      cnt = 6  #additional modules run after the core properties

      #every file gets run with certain properties this puts them first for display
      for key, value in file_obj.iteritems():
        # list format will be [location,key,value] so its sortable
        iList = []
        if key.strip() == "Name":
          iList.append("1")
          iList.append(key.strip())
          iList.append(value)
        else:
          if key.strip() == "_id":
            iList.append("2")
            iList.append(key.strip())
            iList.append(value)
            #iList.append("sam")
          else:
            if key.strip() == "runs":
              iList.append("4")
              iList.append(key.strip())
              iList.append(str(value))
            else:
              if key.strip() == "time":
                iList.append("5")
                iList.append(key.strip())
                iList.append(str(value))
              else:
                if key.strip() == "file-type":
                  iList.append("3")
                  iList.append(key.strip())
                  iList.append(value)
                else:
                  iList.append(str(cnt))
                  iList.append(key.strip())
                  iList.append(value)
                  cnt = cnt + 1
                end
              end
            end
          end
        end
        dList.append(iList)
      end
      dList.sort()

    %>

  <div>
  % for i in range(len(dList)):
  % key = dList[i][1]
  % value = dList[i][2]
    <div class="row">
      <div class="col-12 grid-margin">
        <div class="card">
          <div class="card-body">
            <div>
              <h5 class="font-weight-bold">{{key}}:</h5>
              <div style="margin-left:20px;">
              % if key == "Cuckoo":
 		<p><a href="/download/{{value}}">Cuckoo Report</a></p>

              % else:
                % if isinstance(value, list):
                  % element = value
                  % element.append("spaceForException")
                  <ul>
                     <!-- Use a copy of the list with an extra element to
                    handle an out of range exception  -->
                  % for i in range(len(value)-1):
                    % val = element[i].strip()
                    % nextVal = element[i+1].strip()
                    % if val[:3] == "[+]":
                      % if nextVal[:3] == "[-]":
                        <li>{{ val[3:] }}<ul>
                      % else:
                        <li>{{ val[3:] }}</li>
                      % end
                    % else:
                      % if val[:3] == "[-]":
                        % if nextVal[:3] == "[-]":
                          <li>{{ val[3:] }}</li>
                        % else:
                          <li>{{ val[3:] }}</li></ul>
                        % end
                      % else:
                        <li>{{ val }}</li>
                      % end
                    % end
                  % end

                  </ul>
                %else:
                  <p>{{value}}</p>
                % end
              % end
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  %end
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
<<<<<<< HEAD


<script>

function showRepo(event, linkStr)
{
	event.preventDefault();
	window.location.open(linkStr);
}

function showReport(link) {
	window.location.href = link.substring(0,10);
	alert(link);
}


</script>

=======
>>>>>>> 91251fbd5e6fc79a8ebb4514710d1c67b9dbf57f
