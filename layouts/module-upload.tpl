%include layouts/header

<script src="//code.jquery.com/jquery-1.11.1.min.js"></script>

<div class="content-wrapper">


<div class="container">
      <div class="panel panel-default">
          <!-- Standar Form -->
          <h4>Select files from your computer</h4>
          <form action="/mu" method="post" enctype="multipart/form-data" id="js-upload-form">
            <div class="form-inline">
              <div class="form-group">
                <input type="file" name="files[]" id="js-upload-files" multiple>
              </div>
              <button type="submit" class="btn btn-sm btn-primary" id="js-upload-submit">Upload Files</button>
            </div>
          </form>

          <!-- Drop Zone -->
          <h4>Or drag and drop files below</h4>
          <div class="upload-drop-zone" id="drop-zone">
            Just drag and drop files here
          </div>

          <!-- Upload Finished -->
          <div class="js-upload-finished" id="js-upload-finished">
            <h3>Processed files</h3>
            <div class="list-group">
              <!-- <p href="#" class="list-group-item list-group-item-success"><span class="badge alert-success pull-right">Success</span>image-01.jpg</p>
              <p href="#" class="list-group-item list-group-item-success"><span class="badge alert-success pull-right">Success</span>image-02.jpg</p> -->
            </div>
          </div>
        </div>
      </div>
    </div> <!-- /container -->
  </div> <!-- /container -->


  <script type="text/javascript">

  + function($) {
    'use strict';

    // UPLOAD CLASS DEFINITION
    // ======================

    var dropZone = document.getElementById('drop-zone');
    var uploadForm = document.getElementById('js-upload-form');
    var uploadButton = document.getElementById('js-upload-submit');
    var uploadedFiles = document.getElementById('js-upload-finished');
    var uploads = 0;


    var startUpload = function(files) {
      uploads++;
      console.log(files)

      uploadButton.innerHTML = 'Uploading...';
      dropZone.innerHTML = 'Uploading...';


      var formData = new FormData();

              // Loop through each of the selected files.
      for (var i = 0; i < files.length; i++) {
        var file = files[i];

        // // Check the file type.
        // if (!file.type.match('image.*')) {
        //   continue;
        // }

        // Add the file to the request.
        formData.append('files[]', file, file.name);
      }
      // Set up the request.
      var xhr = new XMLHttpRequest();
      // Open the connection.
      xhr.open('POST', '/mu', true);
      // Set up a handler for when the request finishes.
      xhr.onload = function (e) {
        if (xhr.status === 200) {

          files = JSON.parse(xhr.response)

          for(var file = 0; file < files.length; file++)
          {
            $('#js-upload-finished')
                .find('.list-group')
                .append(
                  '<p href="#" class="list-group-item list-group-item-success"><span class="badge alert-success pull-right">Success</span> '+files[file]+' </p>'
                )
          }
          uploads--;

          if(uploads == 0)
          {
            uploadButton.innerHTML = 'Upload Files';
            dropZone.innerHTML = 'Just drag and drop files here';
          }
        } else {
          alert('An error occurred!');
          uploads--;
        }
      };
      // Send the Data.
      xhr.send(formData);
    }

    uploadForm.addEventListener('submit', function(e) {
      e.preventDefault()
      var files = document.getElementById('js-upload-files').files;

      startUpload(files)
    })

    dropZone.ondrop = function(e) {
        e.preventDefault();
        this.className = 'upload-drop-zone';

        startUpload(e.dataTransfer.files)
    }

    dropZone.ondragover = function() {
        this.className = 'upload-drop-zone drop';
        return false;
    }

    dropZone.ondragleave = function() {
        this.className = 'upload-drop-zone';
        return false;
    }

}(jQuery);
</script>


%include layouts/footer
