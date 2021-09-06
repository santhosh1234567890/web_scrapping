<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <link href="styles.css" rel="stylesheet" />
  
  <link href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap4.min.css" rel="stylesheet" crossorigin="anonymous" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/js/all.min.js" crossorigin="anonymous"></script>
  <!-- <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css"> -->
</head>
<style>
.custom-file {
    position: relative;
    display: inline-block;
    width: 100%;
    height: calc(1.5em + .75rem + 2px);
    margin-bottom: 20px;
    cursor: pointer;
}

.custom-file-input {
    position: relative;
    z-index: 2;
    width: 100%;
    height: calc(1.5em + .75rem + 2px);
    margin: 0;
    opacity: 0;
}
.custom-file-label {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    z-index: 1;
    height: calc(1.5em + .75rem + 2px);
    padding: .375rem .75rem;
    font-weight: 400;
    line-height: 1.5;
    color: #495057;
    background-color: #fff;
    border: 1px solid #ced4da;
    border-radius: .25rem;
    cursor: pointer;
}
.custom-file-label::after {
    position: absolute;
    content: 'Browse';
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 3;
    display: block;
    height: calc(1.5em + .75rem);
    padding: .375rem .75rem;
    line-height: 1.5;
    color: #495057;
    content: "Browse";
    background-color: #e9ecef;
    border-left: inherit;
    border-radius: 0 .25rem .25rem 0;
}

.textTransform{
  text-transform:capitalize;
}
#loading-image{
  top: 0;
    bottom: 0;
    right: 0;
    margin: auto;
    position: absolute;
    left: 0;
    z-index: 2222;
}

.loading-image {
  position: absolute;
  top: 100px;
  left: 240px;
  z-index: 100;
}
</style>
<body class="sb-nav-fixed">
    <nav class="sb-topnav navbar navbar-expand navbar-dark bg-dark">
            <a class="navbar-brand" href="index.php">Scraping</a>
            <button class="btn btn-link btn-sm order-1 order-lg-0" id="sidebarToggle" href="#"><i class="fas fa-bars"></i></button>
            <!-- Navbar Search-->
            <form class="d-none d-md-inline-block form-inline ml-auto mr-0 mr-md-3 my-2 my-md-0">
                <div  class="input-group">
                    <input class="form-control" type="text" placeholder="Search for..." aria-label="Search" aria-describedby="basic-addon2" />
                    <div  class="input-group-append">
                        <button class="btn btn-primary" type="button"><i class="fas fa-search"></i></button>
                    </div>
                </div>
            </form>
            <!-- Navbar-->
            <ul class="navbar-nav ml-auto ml-md-0">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" id="userDropdown" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fas fa-user fa-fw"></i></a>
                    <div class="dropdown-menu dropdown-menu-right" aria-labelledby="userDropdown">
                        <a class="dropdown-item" href="#">Settings</a>
                        <a class="dropdown-item" href="analytics.php">Activity Log</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="login.php">Logout</a>
                    </div>
                </li>
            </ul>
    </nav>
        <div id="layoutSidenav">
            <div id="layoutSidenav_nav">
                <nav class="sb-sidenav accordion sb-sidenav-dark" id="sidenavAccordion">
                    <div class="sb-sidenav-menu">
                        <div class="nav">
                            <div class="sb-sidenav-menu-heading"><Menu</div>
                            <a class="nav-link" href="index.html">
                                <div class="sb-nav-link-icon"><i class="fas fa-tachometer-alt"></i></div>
                                Dashboard
                            </a>
                            <a class="nav-link" href="webpage.php">
                                <div class="sb-nav-link-icon"><i class="fas fa-tachometer-alt"></i></div>
                                Scraping
                            </a>
                            <a class="nav-link" href="connection.php">
                                <div class="sb-nav-link-icon"><i class="fas fa-tachometer-alt"></i></div>
                                audit_log
                            </a>
                          </div>
                    </div>
                    <div class="sb-sidenav-footer">
                        <div class="small">Logged in as:</div>
                        Bitwise
                    </div>
                </nav>
            </div>
            <div id="layoutSidenav_content">
            <div class="container-fluid">
                    <h1 class="mt-4">Scraping</h1>
                    <ol class="breadcrumb mb-4">
                    <li class="breadcrumb-item"><a href="#">Dashboard</a></li>
                    <li class="breadcrumb-item active">Scraping</li>
                    </ol>                   
                    <div class="container" style="margin: -25px;margin-top: 5px">
                      <h3>Enter Your keyword</h3>
                      <p>The keyword contains like machine learning, deep learning, svm with finance etc</p>
                      <form id="api_form">
                      <div class = "row">
                        <div class = "col-md-3">
                        <div class="form-group pb-3">
                        <select class="form-control" id="type">
                          <option value = "0" disabled selected >Select content-type</option>
                          <option value = "multi">All</option>
                          <option value = "pdf">Pdf</option>
                          <option value = "program">Program</option>
                          <option value = "text">Text</option>
                          <option value = "videos">Videos</option>
                        </select>
                      </div>
                      </div>
                      <div class = "col-md-3">
                        <div class="form-group pb-3">
                        <select onchange="checkcustom()" class="form-control" id="search-engine">
                          <option value = "0" disabled selected >Select Search-engine</option>
                          <option value = "custom">Custom</option>
                          <option value = "bing">Bing</option>
                          <option value = "duckduckgo">Duckduckgo</option>
                          <option value = "google">Google</option>
                        </select>
                        </div>  
                      </div>
                      <div id="custominput" style="display:active;" class = "col-md-3">
                      <div class="custom-file">
                          <input type="file" onchange="readText(event)" class="custom-file-input" id="customFile" name="filename">
                          <label class="custom-file-label" for="customFile">Choose File</label>
                      </div>
                      </div>
                      <div class = "col-md-3 ">
                          <div style="display:flex;">
                          <input type="text" class="form-control" id="search_value" placeholder="Enter Query" name="search" style="margin-bottom: 20px:width: fit-content;">
                          <div style="margin-left:-3px;">
                          <button style="white-space: nowrap;" class="btn btn-primary" type="submit">
                          <span>
<svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" viewBox="0 0 24 24" fill="#fff"><g data-name="Layer 2"><g data-name="download"><rect width="24" height="24" opacity="0"></rect><rect x="4" y="18" width="16" height="2" rx="1" ry="1"></rect><rect x="3" y="17" width="4" height="2" rx="1" ry="1" transform="rotate(-90 5 18)"></rect><rect x="17" y="17" width="4" height="2" rx="1" ry="1" transform="rotate(-90 19 18)"></rect><path d="M12 15a1 1 0 0 1-.58-.18l-4-2.82a1 1 0 0 1-.24-1.39 1 1 0 0 1 1.4-.24L12 12.76l3.4-2.56a1 1 0 0 1 1.2 1.6l-4 3a1 1 0 0 1-.6.2z"></path><path d="M12 13a1 1 0 0 1-1-1V4a1 1 0 0 1 2 0v8a1 1 0 0 1-1 1z"></path></g></g></svg>
</span>Start scrape</button>
                          </div>
                          </div>
                      </div>
                      </div>
                      <p><a href="customfile.json" class="btn btn-primary" download="customfile.json">Download Custom file</a></p>
                      <!-- <p style="font-size:20px;color:DodgerBlue"><b>Note : For custom search engine,File must be in this format only eg: [" ", " "]</b></p> -->
                      </form>
                      <div class="card mb-4">
                      <div class="card-header">
                        <i class="fas fa-table mr-1"></i>
                        Tagging Documents
                      </div>
                    <div class="card-body">
                      <table id ="td" style="margin: 20px;" class="table table-striped table-bordered mydatatable">
                        <thead>
                            <tr>
                              <th scope="col">#</th>
                              <th scope="col">Title</th>
                              <th scope="col">Content type</th>
                              <th scope="col">Individual Tags</th>
                              <th scope="col">No of Tags</th>
                              <th scope="col">Content Category</th>
                            </tr>
                          </thead>
                        <tbody id="api_content">
                        </tbody>
                    </table>
                    </div>
                    <div id="loading" style = "display:none">
                      <img id="loading-image" src="1488.gif" alt="Loading..." />
                    </div>
              </div>
          </div>
      </div>
  </div>
</div>
</script>
</body>
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
<script src="js/scripts.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js" crossorigin="anonymous"></script>
<script src="https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap4.min.js" crossorigin="anonymous"></script>
<script src ="http://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script>

//this function will display the choose file option if the search engine will be custom else it will not display the box 
function checkcustom(){
  if($('#search-engine').val()=="custom"){
    document.getElementById('custominput').style.pointerEvents='auto';
  }else{
    document.getElementById('custominput').style.pointerEvents='none';
  }
}

//Allow to access the datatables for the webpage 

$('.mydatatable').wrap('<div id="hide" style="display:none"/>');
 var ScrapTable =  $('.mydatatable').DataTable({
   "columnDefs": [{ className: "textTransform", "targets": [ 2 ] }]//showinng the contenttype value as caps
 });
 
//reading the file content from webpage input for custom search engine
var text=0;
async function readText(event) {
  const file = event.target.files.item(0)
  text = await file.text();
}

//this function will appeaar name of the file appear on select
$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

//This function will get the input values from the webpage for scraping and  posting the scraping values without page refresh
$('#api_form').submit(function(e){
  e.preventDefault();
  var data;
  // if the search engine will be custom the file have to passed for the input or scraping else file parameter is false
  if(document.getElementById('search-engine').value=="custom"){
    data={
    'search':document.getElementById('search_value').value,//passing the input value for the query
    'type':document.getElementById('type').value,//passing the input for the content-type
    'engine':document.getElementById('search-engine').value,//passing the input value for the search engine
    'file':text//passing the input file content for the custom search engine
  }
  }else{
    data={
    'search':document.getElementById('search_value').value,
    'type':document.getElementById('type').value,
    'engine':document.getElementById('search-engine').value,
    'file':false
  }
  }
  document.getElementById('loading').style.display ="block";

  $('.mydatatable').DataTable().clear();
  var final_data="";
  $.ajax({
    type:"GET",
    url:"action_page.php",
    data:data,
    success:function(data){
    // console.log(data);
      var obj = JSON.parse(data);
    final_data = JSON.parse(obj.data);
     console.log(final_data)
    //  document.getElementById('#api_content').innerHTML="";
     var row="";
     //For displaying values in the webpage in datatable from the scraping and tagging results
    document.getElementById('td').style.display="inline-table";
     document.getElementById('loading').style.display ="none";
     $('#hide').css('display','block');
     for(var i =0 ; i<final_data.length; i++){
        var obj = final_data[i][0].tag_details.tags;
        ScrapTable.row.add([''+(i+1)+'','<a href="'+final_data[i][0].url+'" target="_blank">'+final_data[i][0].title+'</a>',''+final_data[i][0].content_type+'',''+final_data[i][0].tag_details.individual_tags+'',''+final_data[i][0].tag_details.no_of_tags+'','-']);
        ScrapTable.draw();
      //  for(var  j =0; j<obj.length ; j++){
       
     // row = `<tr><th scope="row">`+i+`</th><td><a href="`+final_data[i][0].url+`" target="_blank">`+final_data[i][0].title+`</a></td><td>`+final_data[i][0].content_type+`</td><td>`+final_data[i][0].tag_details.individual_tags+`</td><td>`+final_data[i][0].tag_details.no_of_tags+`</td><td>-</td></tr>`;
          // console.log(obj[j]);
      //   }
   ///    document.getElementById('api_content').innerHTML+=row;
     }
    
      // console.log(JSON.stringify(data));
      // console.log(JSON.parse(data))
      // var obj = data["data"]
      // for(var  i =0; i<obj.length ; i++){
      //   console.log(obj[i])
      // }
    },
    error:function(e){
      console.log(e)
    }
  })
})

</script>
</html>

