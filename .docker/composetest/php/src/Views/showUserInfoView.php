<?php
session_start();
?>
<!DOCTYPE HTML>  
<html>
  <head>
    <style>
      .error {color: #FF0000;}
    </style>
  </head>
<body>

  
  <h2>Deine Infos</h2>

  <?php
    $userInfo = $_SESSION["userInfo"];
    foreach($userInfo as $infoArray){
      foreach($infoArray as $info){
        echo "<br>";
        print($info);
        echo "<br>";
      }
    }
?>

</body>
</html>