    <?php 
    $result= $_GET['search'];//getting the query from the webpage
    $result1 = $_GET['type'];//getting the contenttype from the webpage
    $result2 = $_GET['engine'];//getting the search engine from the webpage
    // echo $_GET['file'];
    $result3 = $_GET['file'];//getting the file from the webpage
    $result= strtolower($result);
    //passing the input values to the flask using curl command for scraping
    $data = array("query"=> $result,"lang"=>"en","content_type"=> $result1,"search_engine"=> $result2,"filename"=> $result3);
    $curl = curl_init();
    curl_setopt_array($curl, array(
    CURLOPT_URL => 'http://127.0.0.1:5000/knowledge-base',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_ENCODING => '',
    CURLOPT_MAXREDIRS => 10,
    CURLOPT_TIMEOUT => 0,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
    CURLOPT_CUSTOMREQUEST => 'POST',
    CURLOPT_POSTFIELDS =>json_encode($data),
    CURLOPT_HTTPHEADER => array(
        'Content-Type: application/json'
    ),
    ));

        $response = curl_exec($curl);
        curl_close($curl);
         //print_r($response);
      //  echo json_encode('45');
        //echo $response;
        $data = array();
        $data = array("sucess"=>true,"data"=> $response );
        echo json_encode($data);
    //
    // json_decode($response)
    ?>
