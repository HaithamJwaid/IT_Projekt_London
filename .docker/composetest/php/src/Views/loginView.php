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

  <form method="post" action="../login.php">
    <label for="userId">User Id:</label><br> 
    <input type="userId" id="userId" name="userId" value=""><br>
    <input type="submit" name="submit" value="Submit">  
  </form> 

</body>
</html>