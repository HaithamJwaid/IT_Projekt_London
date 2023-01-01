<?php
  include "dbConnection.php";
  session_start();
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
     $productname = $_POST["searchProduct"];
     $connector = new Connector();
     
     $_SESSION["searchProduct"] = $productname;
     //$_SESSION["msg"] = $connector->search($id);
     $_SESSION["products"] = $connector->searchForProduct($productname);
     
     header("Location: Views/webshopView.php");
     exit();
  }else{
    session_destroy();
    header("Location: Views/webshopView.php");
    exit();
    //echo file_get_contents("Views/indexView.php");
  }
