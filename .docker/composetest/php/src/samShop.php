<?php
  include "dbConnection.php";
  session_start();
  if ($_SERVER["REQUEST_METHOD"] == "POST") {

     $connector = new Connector();
     
     if(isset($_REQUEST['addItem'])) {
      $productname = $_POST["productName"]; 
      $productprice = $_POST["productPrice"];
      $_SESSION["addproduct"] = $connector->addItem($productname, $productprice);
    }
    else {
     $productname = $_POST["searchProduct"];
     $_SESSION["searchProduct"] = $productname;
     //$_SESSION["msg"] = $connector->search($id);
     $_SESSION["products"] = $connector->samSearchForProduct($productname);
    }
    
     header("Location: Views/samShopView.php");
     exit();
  }else{
    
    header("Location: Views/samShopView.php");
    exit();
    //echo file_get_contents("Views/indexView.php");
  }