<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
</head>


<body>
        
        <br>
        <br>
        <br><br>

        <h2>User info</h2>

        <?php

/*
            $user = [];
            $user["First_Name"] = "FUCK";
            $user["Last_Name"] = "My";
            $user["DoB"] = "Life";
            */
            $user = $_SESSION["user"];
            

            if($user != NULL) {

                        echo "<table BORDER =2>" ;
            echo "<tr>";
                echo "<th>First Name </th> <th>Last Name</th> <th>Date of Birth</th>";
            echo "</tr>";
            
    
            echo "<tr>";
            echo "<td>" . $user["First_Name"]. "</td>";
            echo "<td>" . $user["Last_Name"]. "</td>";
            echo "<td>" . $user["DoB"]. "</td>";
            echo "</tr>";
            echo "</table>" ;
      } else echo "Einlog daten falsch !";
           
       ?>
       
    </body>
</html>