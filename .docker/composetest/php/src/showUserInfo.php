<?php
  include "dbConnection.php";
  //session_destroy();
  session_start();
  //$userName = $_SESSION["username"];
  #$userName = "franz";
  $userName = 'franz'. "' UNION SELECT *, Null as Col4, NUll as Col5, Null as col6, Null as col7 FROM user_login -- ";
  #$userName = $_SESSION["userName"];
  $connector = new Connector();
  $userInfo = $connector->getUserInfo($userName);
  $_SESSION["userInfo"] = $userInfo;

  header("Location: Views/showUserInfoView.php");
  