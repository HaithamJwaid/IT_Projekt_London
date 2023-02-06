<?php
  include "dbConnection.php";
  session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {

   // Check if username is empty
   if(empty(trim($_POST["username"]))){
   echo "Please enter username.";
} else{
    $username = trim($_POST["username"]);
}

// Check if password is empty
if(empty(trim($_POST["password"]))){
    echo "Please enter your password.";
} else{
    $password = trim($_POST["password"]);
}


if(isset($username) && isset($password)){
     $connector = new Connector();
          
     if($connector->validateLogin($username, $password)){
     
       header("location: Views/samShopView.php");
        } 
else{
    //$_SESSION["loginError"] = TRUE;
    header("location: Views/loginView.php");
}}
    exit();
    //echo file_get_contents("Views/indexView.php");
  }
