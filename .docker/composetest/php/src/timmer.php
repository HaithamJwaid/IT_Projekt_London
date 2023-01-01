<?php
  include "dbConnection.php";
  session_start();

  // define variables and set to empty values
  $nameErr = "";
  $name = "";

  if ($_SERVER["REQUEST_METHOD"] == "POST") {
     $id = $_POST["id"];
     $connector = new Connector();
     $connector->bulshit($id);
     $_SESSION["id"] = $id;

     header("Location: Views/timerIndex.php");
     exit();
  }else{
    header("Location: Views/timerIndex.php");
    exit();
  }
