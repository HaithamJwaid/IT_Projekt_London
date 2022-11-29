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

  <form method="post" action="../index.php">
    <label for="id">ID:</label><br> 
    <input type="text" id="id" name="id" value=""><br>
    <input type="submit" name="submit" value="Submit">  
  </form> 
  <h2>Your Massage:</h2>

  <?php
  if(isset($_SESSION["id"])){
    if($_SESSION["id"] != NULL){
      $msg = $_SESSION["msg"];
      for($i = 0; $i < count($msg); $i++){
          echo "<br>";
          echo "Your Message is: " . $msg[$i]["Msg"];
          echo "<br>";
      }
    }
  }
?>

</body>
</html>