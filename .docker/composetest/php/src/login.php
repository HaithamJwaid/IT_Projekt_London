<?php
  include "dbConnection.php";
  session_start();

  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $userId = $_POST["userId"];
    $connector = new Connector();
    $userName = $connector->getUserNameFromId($userId);

    $_SESSION["userName"] = $userName;

    header("Location: showUserInfo.php");
    exit();
 }else{
   header("Location: Views/loginView.php");
   exit();
 }


