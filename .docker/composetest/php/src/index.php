<?php
  include "dbConnection.php";
  //session_destroy();
  session_start();
  // define variables and set to empty values
  $nameErr = "";
  $name = "";

  if ($_SERVER["REQUEST_METHOD"] == "POST") {
     $id = $_POST["id"];
     $connector = new Connector();
     
     $_SESSION["id"] = $id;
     $_SESSION["msg"] = $connector->search($id);
     //$_SESSION["msg"] = $connector->saveSearch($id);

     header("Location: Views/indexView.php");
     exit();
  }else{
    header("Location: Views/indexView.php");
    exit();
  }
