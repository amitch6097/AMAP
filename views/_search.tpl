
<div class="col-8" style="margin: 0 auto; margin-top: 100px;" >

  <div class="card"style="border-radius:10px; padding:10px;" >
    <h4 class="card-title" >Malware Search</h4>
    <div class="card-body" style="overflow: scroll; height:600px; text-align:left; border:1px solid #e8e8e8">



  <!--TODO not output but button leading to page -->
  %if len(search_output) == 0:
  <div class="row">
    <div class="col-12 grid-margin">
      <div class="card">
        <div class="card-body">
            <h4 class="card-title">No Matching Files</h4>
          </div>
        </div>
      </div>
    </div>
  %else:
  %for obj in search_output:
  % id = obj['_id']
    <form  id="{{id}}" enctype="multipart/form-data" >
    <div class="row">
      <div class="col-12 grid-margin" style="margin-bottom:0px;">
        <div class="card" style="padding:0px 0px;">
          <div class="card-body" style="padding:0px 0px;">

            <div class="form-row align-items-center">
              <label class="form-check-label">
                  <h4>{{obj['Name']}}</h4>
              </label>
              <div class="col-auto ml-auto">
                <button type="button" onclick="fileView(event, '{{id}}')" class="btn btn-info btn-fw" style="min-width: 12px;">View</button>
                <input type="hidden" name="filename" value={{obj['Name']}}>
              </div>
            </div>
            <div style="margin-left:15px">
              %if "sha256" in obj.keys():
              <p>SHA256: {{obj['sha256']}}</p>
              %else:
                %pass
              %end
              %if "sha1" in obj.keys():
              <p>SHA1: {{obj['sha1']}}</p>
              %else:
                %pass
              %end
              %if "md5" in obj.keys():
              <p>MD5: {{obj['md5']}}</p>
              %else:
                %pass
              %end
            </div>
            <hr style="z-index: 3 !important; height:1px;">
          </div>
        </div>
      </div>
    </div>
  </form>


  %end
  %end
</div>
</div>
</div>
