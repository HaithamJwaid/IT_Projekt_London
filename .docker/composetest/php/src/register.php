<?php
    include "dbConnection.php";
  session_start();
  if ($_SERVER["REQUEST_METHOD"] == "POST") {

     $connector = new Connector();

     if (isset($_REQUEST['submit'])) {
        $username = $_POST['username'];
        $email = $_POST['email'];
        $password = $_POST['password'];
      
        if ($connector->add_user($username, $email, $password)) {
          echo "Registrierung erfolgreich";
        } else {
          echo "Registrierung fehlgeschlagen";
        }
      }
      
     header("Location: Views/registerView.php");
     exit();
  }else{
    
    header("Location: Views/registerView.php");
    exit();
    //echo file_get_contents("Views/indexView.php");
  }