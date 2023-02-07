<?php

session_start();
?>

<!DOCTYPE html>
<html>
    <head>
        <style>
            h1 {
                color:darkblue ;
                font-family: 'Times New Roman', Times, serif;
                margin:45px;
                margin-top: 50px;
                text-align: center;
            }

        </style>
    <title>Login Site</title>
    </head>

<body>
    <h1>Login</h1>
    <form method="post" action="/login.php">
    <label for="username"> Username: </label>
    <input type="text" id="username" name="username" size="50"> <br>

    <label for="password"> Password:  </label> 
    <input type="password" id="password" name="password" size="50"><br>
    <br>
    <br>
    <input type="submit" value="Login" name="login" >
   </form>

   <?php
   if(isset($_SESSION["loginError"]) && $_SESSION["loginError"])
   echo "Username or password incorrect";
   ?>

</body>
</html>