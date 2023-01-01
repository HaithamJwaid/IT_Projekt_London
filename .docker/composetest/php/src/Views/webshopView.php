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

       <form method="post" action="/indexWebshop.php">
        <label for="searchProduct"> Search: </label>
        <input type="text" id="searchProduct" name="searchProduct" size="50"> <br>
        <input type="submit" value="Search" name="submit" >
</form>
        <br><br>

        <h2>Products</h2>

        <?php

            if(isset($_SESSION["searchProduct"])){
            if($_SESSION["searchProduct"] != NULL){
            $products = $_SESSION["products"];

            if($products != NULL) {

                        echo "<table BORDER =2>" ;
            echo "<tr>";
                echo "<th>First Name </th> <th>Last Name</th> <th>Date of Birth</th>";
            echo "</tr>";
            
    
        
                for($i = 0; $i < count($products); $i++){
                    echo "<tr>";
                        echo "<td>" . $products[$i]["First_Name"]. "</td>";
                        echo "<td>" . $products[$i]["Last_Name"]. "</td>";
                        echo "<td>" . $products[$i]["DoB"]. "</td>";
                        echo "</tr>";
                }
            echo "</table>" ;
      } else echo "Product not found";
           
 }   
    
  }
       ?>
       
    </body>
</html>