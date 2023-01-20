<?php

session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        h1,h2{
            text-align: center;
            color: solid black;
        }
        table{
            margin-left:auto;
            margin-right:auto;
        }
        tr{
            font-size: 20px;
        }
        p{
            text-align: center;
        }
    </style>
</head>


<body>
        
        <br>
        <h1> Webshop </h1>
        <br>
        <br>

    <form method="post" action="/indexWebshop.php">
        <p> Search: 
        <input type="text" id="searchProduct" name="searchProduct" size="75"> 
        <input type="submit" value="Search" name="submit" >
    </form>
        <br><br>

        <h2>Products</h2>
        <br>

        <?php

            if(isset($_SESSION["searchProduct"])){
            if($_SESSION["searchProduct"] != NULL){
            $products = $_SESSION["products"];

            if($products != NULL) {

                        echo "<table BORDER =2>" ;
            echo "<tr>";
                echo "<th>Product </th> <th>Price</th> <th>Quantity</th>";
            echo "</tr>";
            
    
                for($i = 0; $i < count($products); $i++){
                    echo "<tr>";
                        echo "<td>" . $products[$i]["Product_name"]. "</td>";
                        echo "<td>" . $products[$i]["Price"]. "</td>";
                        echo "<td>" . $products[$i]["Quantity"]. "</td>";
                        echo "</tr>";
                }
            echo "</table>" ;
            } else echo "Product not found";
           
            }   
            }
       ?>

        <br><br><br>
        <form method = "post" action= "/indexWebshop.php">
        <p> Add Product:
        <br> <br>
        <label for= "productName"> Name: </label>
        <input type="text" id="productName" name="productName" >
        <label for= "productprice"> Price: </label>
        <input type="text" id="productPrice" name="productPrice">
        <input type="submit" value="Add Item" name="addItem" >
    </form>
       
    </body>
</html>
