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
  <link rel="stylesheet"  href="css/cover.css">
  <!-- endinject -->
  <link rel="shortcut icon" href="images/favicon.png" />
</head>
<body>
  <script src="https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"></script>
  <script src="node_modules/bootstrap/dist/js/bootstrap.min.js"></script>

  <script src="filePage.js"></script>
  <body class="text-center">

      <div class="cover-container d-flex h-100 p-3 mx-auto flex-column">
        <header class="masthead mb-auto" style="z-index:2;">
          <div class="inner">
            <img class="masthead-brand" src="images/accenture_logo_white.png" width="150px" alt="logo"/><h3 style="margin:15px 0px 0px 15px;" class="masthead-brand">AMAP</h3>

            <!-- <h3 class="masthead-brand">Accenture AMAP</h3> -->
            <nav class="nav nav-masthead justify-content-center" style="z-index:2;">
              <a class="nav-link active" id="Dashboard" onClick="pageSelector(event,'Dashboard')" href="">Dashboard</a>
              <a class="nav-link" id="Files" onClick="pageSelector(event, 'Files')" href="">Files</a>
              <a class="nav-link" id="Modules" onClick="pageSelector(event,'Modules')" href="">Modules</a>
              <a class="nav-link" href="/login">Logout</a>
            </nav>
          </div>
        </header>

        <div id="page-dashboard" style="position: relative;width: 100%;">
        </div>
        <div id="page-files" style="display:none; position: relative;width: 100%;">
        </div>
        <div id="page-modules" style="display:none; position: fixed;width: 100%;">
        </div>
      </div>
    </body>

<script>
$( "#page-dashboard" ).load( "dashboard.html" );
$( "#page-files" ).load( "file-page.html" );
$( "#page-modules" ).load( "modules-page.html" );

var processInterval;

var pageSelector = function(event, pageName)
{
  event.preventDefault()

  if(pageName == "Dashboard")
  {
    $( "#page-dashboard" ).css( "display", "block");
    $( "#page-files" ).css( "display", "none");
    $( "#page-modules" ).css( "display", "none");

    $( "#Dashboard" ).addClass('active')
    $( "#Files" ).removeClass('active')
    $( "#Modules" ).removeClass('active')
    clearInterval(processInterval);
    $.getScript("js/dashboard.js", function(){
    });
  }
  else if (pageName === "Files")
  {
    $( "#page-dashboard" ).css( "display", "none");
    $( "#page-files" ).css( "display", "block");
    $( "#page-modules" ).css( "display", "none");

    $( "#Dashboard" ).removeClass('active')
    $( "#Files" ).addClass('active')
    $( "#Modules" ).removeClass('active')

    processInterval = setInterval(getProcesses, 5000);
  }
  else if (pageName === "Modules")
  {
    $( "#page-dashboard" ).css( "display", "none");
    $( "#page-files" ).css( "display", "none");
    $( "#page-modules" ).css( "display", "block");

    $( "#Dashboard" ).removeClass('active')
    $( "#Files" ).removeClass('active')
    $( "#Modules" ).addClass('active')
    clearInterval(processInterval);
  }
}

var countOpen = 0;

function showModules(event, i)
{
  event.preventDefault()
  var id = "#"+i.toString()+"row"
  console.log(countOpen)

  var dis = $(id).css('display')

  if(dis==='block'){
    countOpen-=1
    $(id).css('display', "none")
    if(countOpen<=0)
    {
      processInterval = setInterval(getProcesses, 5000);
    }
  }else if(dis==='none'){
    countOpen+=1
    clearInterval(processInterval);
    $(id).css('display', "block");
  }
}
</script>
