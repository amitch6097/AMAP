<!DOCTYPE html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>AMAP</title>
  <!-- plugins:css -->
  <link rel="stylesheet" href="node_modules/mdi/css/materialdesignicons.min.css">
  <link rel="stylesheet" href="node_modules/perfect-scrollbar/dist/css/perfect-scrollbar.min.css">
  <!-- endinject -->
  <!-- plugin css for this page -->
  <link rel="stylesheet" href="node_modules/jquery-bar-rating/dist/themes/css-stars.css">
  <link rel="stylesheet" href="node_modules/bootstrap-datepicker/dist/css/bootstrap-datepicker.min.css" />
  <!-- End plugin css for this page -->
  <!-- inject:css -->
  <link rel="stylesheet" href="css/style.css">
  <!-- endinject -->
  <link rel="shortcut icon" href="images/favicon.png" />
</head>
<body>
  <div class="container-scroller">
    <!-- partial:partials/_navbar.html -->
    <nav class="navbar col-lg-12 col-12 p-0 fixed-top d-flex flex-row">
      <div class="text-center navbar-brand-wrapper d-flex align-items-center justify-content-center">
        <a class="navbar-brand brand-logo" href="/dashboard"><img src="images/accenture_logo.png" alt="logo"/></a>
        <a class="navbar-brand brand-logo-mini" href="/"><img src="images/logo-mini.svg" alt="logo"/></a>
      </div>
      <div class="navbar-menu-wrapper d-flex align-items-stretch">
        <div class="search-field ml-4 d-none d-md-block">
          <!-- action="" method="post" enctype="multipart/form-data" id="js-upload-form" -->
          <form class="d-flex align-items-stretch h-100" action="/malware-search" method="post" onsubmit="submitSearch()" enctype="multipart/form-data">
            <div class="input-group">
              <input type="text" name="module-search-input" class="form-control bg-transparent border-0" placeholder="Search">
              <input type="hidden" id="malware-search-type" name="malware-search-type" value="File Name">
              <div class="input-group-btn">
                <button id="malware-search-button" style="width:100px;"type="button" class="btn bg-transparent dropdown-toggle px-0" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <i class="mdi mdi-earth"></i>
                  File Name
                </button>
                <!-- Andrew Fix ALPHA -->
                <div class="dropdown-menu dropdown-menu-right">
                  <a class="dropdown-item" href="" id="search-category" onClick="changeName(event, 'File Name')">File Name</a>
                  <a class="dropdown-item" href="" id="search-category" onClick="changeName(event, 'MD5')">MD5</a>
                  <a class="dropdown-item" href="" id="search-category" onClick="changeName(event, 'SHA1')">SHA1</a>
                  <a class="dropdown-item" href="" id="search-category" onClick="changeName(event, 'SHA256')">SHA256</a>
                  <!-- <div role="separator" class="dropdown-divider"></div>
                  <a class="dropdown-item" href="#">Month and older</a> -->
                <!-- </div> -->
              </div>

              <script>
              function changeName(event, new_name) {
                event.preventDefault()
                document.getElementById("malware-search-button").innerHTML = '<i class="mdi mdi-earth"></i> ' + new_name + ' '
                document.getElementById("malware-search-type").value = new_name

              }
              </script>

              <div class="input-group-addon bg-transparent border-0 search-button">
                <button type="submit" class="btn btn-sm bg-transparent px-0">
                  <i class="mdi mdi-magnify"></i>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
      <ul class="navbar-nav">
      <a class="nav-link active" id="Dashboard" onClick="pageSelector(event,'Dashboard')" href="">Dashboard</a>
      <a class="nav-link" id="Files" onClick="pageSelector(event, 'Files')" href="">Files</a>
      <a class="nav-link" id="Modules" onClick="pageSelector(event,'Modules')" href="">Modules</a>
    </ul>
        <ul class="navbar-nav navbar-nav-right">
          <li class="nav-item d-none d-lg-block full-screen-link">
            <a class="nav-link">
              <i class="mdi mdi-fullscreen" id="fullscreen-button"></i>
            </a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle nav-profile" id="profileDropdown" href="#" data-toggle="dropdown" aria-expanded="false">
              <!-- <img src="images/faces/face1.jpg" alt="image"> -->
              <span class="d-none d-lg-inline">Andrew Mitchell</span>
            </a>
            <div class="dropdown-menu navbar-dropdown w-100" aria-labelledby="profileDropdown">
              <a class="dropdown-item" href="/my-modules">
                <!-- <i class="mdi fa-code mr-2 text-success"></i> -->
                My Modules
              </a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="/login">
                <i class="mdi mdi-logout mr-2 text-primary"></i>
                Signout
              </a>
            </div>
          </li>
          <li class="nav-item nav-logout d-none d-lg-block">
            <a class="nav-link" href="#">
              <i class="mdi mdi-power"></i>
            </a>
          </li>
        </ul>
        <button class="navbar-toggler navbar-toggler-right d-lg-none align-self-center" type="button" data-toggle="offcanvas">
        <span class="mdi mdi-menu"></span>
      </button>
      </div>
    </nav>
