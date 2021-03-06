<div class="col-8" style="margin: 0 auto; margin-top: 100px;" >

  <div class="card"style="border-radius:10px; padding:10px;" >
    <h4 class="card-title" >{{file_obj['Name']}}</h4>
      <button type="button" onclick="submitReRun(event)" class="btn btn-success">Start New Process</button>
    <div class="card-body" style="overflow: scroll; height:600px; text-align:left; border:1px solid #e8e8e8">

  <form action="/file-rerun" id="file-rerun-form" method="post" enctype="multipart/form-data">

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
        <div class="card">
          <div class="card-body" style="padding:0px;">
            <div>
              <h5 class="font-weight-bold">{{key}}:</h5>
              <div style="margin-left:20px;">
              % if key == "Cuckoo":
                <p><a href="{{value}}">Cuckoo Report</a></p>
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
  %end
  </div>

  </form>


  </div>
</div>
</div>


<script>
function submitReRun(event) {
  event.preventDefault()
  $form = $("#file-rerun-form");

  $.ajax({
      type: 'POST',
      cache: false,
      url:"_file-rerun",
      data: 'id=header_contact_send&'+$form.serialize(),
      success: function(msg) {
        $( "#overlay" ).html( msg);
        document.getElementById("overlay").style.display = "block";
        return false
      }
  });
  return false
}
</script>
