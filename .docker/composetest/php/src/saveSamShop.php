<?php
  include "dbConnection.php";
  session_start();
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    

    
    function test_input($data) {
      $data = trim($data);
      $data = stripslashes($data);
      $data = htmlspecialchars($data);
      //$data = mysql_real_escape_string($data);

      return $data;
    }
     $connector = new Connector();
     
     if(isset($_REQUEST['addItem'])) {
      $productname = test_input($_POST["productName"]); 
      $productprice = $_POST["productPrice"];
      $_SESSION["addproduct"] = $connector->saveAddItem($productname, $productprice);
    }
    else {
     $productname = $_POST["searchProduct"];
     $_SESSION["searchProduct"] = $productname;
     $_SESSION["products"] = $connector->saveSearchForProduct($productname);
    }
    
     header("Location: Views/saveShopView.php");
     exit();
  }else{
    
    header("Location: Views/saveShopView.php");
    exit();
  }