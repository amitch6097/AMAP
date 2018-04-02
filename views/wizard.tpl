%include header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">AMAP Wizard</h3>
  </div>
  <div class="row">
    <div class="col-12 grid-margin">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title" id="wizard-title">Welcome to the Automated Malware Analysis Platform</h4>
          <h4 class="card-title" id="wizard-intra-title" style="display:none">AMAP Wizard</h4>
          <div>
            <form action="/amap-active" method="post" enctype="multipart/form-data">
              % if running == True:
              <!-- AMAP is currently running... -->
              <div class="amap-running" style="display: inline-block" >
                <label>AMAP is currently runnning. Would you like to quit?</label>
                <br>
                <ul class="list-group-flush">
                  <lh>Active Modules:</lh>
                % for module in active_modules:
                  <li class="list-group-item">{{ module }}</li>
                % end
                <br>
                <div class="col-auto ml-auto">
                  <input type="submit" name="enter" class="btn btn-primary" value="Return to Dashboard">
                  <input type="submit" name="enter" class="btn btn-danger" value="Quit AMAP">
                </div>
              </div>
              % end

              % if running == False:
              <div class="amap-stopped">
                  <!-- Module Section -->
                  <div id="modules-select" style="display:block">
                    <label>Available Modules:</label>
                    <!-- add the modules and select here -->
                    <div class="form-group">
                      % for index, option in enumerate(module_options):
                      % name = "{0}".format(index)

                      <div class="form-check form-check-flat">
                        <label class="form-check-label">
                          <input type="checkbox" class="form-check-input" name='{{name}}' checked>
                          {{option}}
                        </label>
                      </div>
                      % end
                    </div>
                    <button type="button" class="btn btn-primary" onclick="onNextToConfig()">Next</button>
                    <!-- <p id="demo" onclick="myFunction()">Click me to change my text color.</p>               -->
                  </div>

                  <div id="config-file-watch" style="display:none">
                    <label>Optional: Leave blank for recommended settings</label>
                    <div>
                      <label>Number of files to select:</label>
                      <input id="files-to-select" name="files-to-select" type="text">
                    </div>
                    <div>
                      <label>Time between each pull:</label>
                      <input id="time-between-select" name="time-between-select" type="text">
                    </div>

                    <button type="button" class="btn btn-primary" onclick="onBackToModules()">Back</button>
                    <button type="button" class="btn btn-primary" onclick="onNextToConfirm()">Next</button>
                    <!-- <p id="demo" onclick="myFunction()">Click me to change my text color.</p>               -->
                  </div>


                  <!-- Confirmation Section -->
                  <div id="confirmation" style="display:none">
                    <label>Are you sure you want to continue?</label>

                    <div class="col-auto ml-auto" id="submit-button">
                      <button type="button" class="btn btn-primary" onclick="onBackToConfig()">Back</button>
                      <input type="submit" name="enter" value="Submit" class="btn btn-success">
                    </div>
                  </div>

                  <!-- TODO: add ability to upload module -->
                  <!-- TODO: where the malware will be coming from -->
                
            </div>
            % end
          </form>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
function onNextToConfig() {
  // alert("HELLO");
    document.getElementById("wizard-title").style.display = "none";
    document.getElementById("wizard-intra-title").style.display = "block";
    document.getElementById("modules-select").style.display = "none";
    document.getElementById("config-file-watch").style.display = "block";
    document.getElementById("confirmation").style.display = "none";
}

function onNextToConfirm() {
  // alert("HELLO");
    document.getElementById("modules-select").style.display = "none";
    document.getElementById("config-file-watch").style.display = "none";
    document.getElementById("confirmation").style.display = "block";
}

function onBackToModules() {
    document.getElementById("wizard-title").style.display = "block";
    document.getElementById("wizard-intra-title").style.display = "none";
    document.getElementById("modules-select").style.display = "block";
    document.getElementById("config-file-watch").style.display = "none";
    document.getElementById("confirmation").style.display = "none";
}

function onBackToConfig() {
  // alert("HELLO");
    document.getElementById("modules-select").style.display = "none";
    document.getElementById("confirmation").style.display = "block";
    document.getElementById("submit-button").style.display = "none";
}

</script>


%include footer