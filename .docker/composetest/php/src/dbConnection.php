<?php

    class Connector{

        #static $host =       "db";
        static $host =       "mariadb";
        static $user =       "root";
        static $pass =       "Darius1998";
        static $mydatabase = "MY_DATABASE";

        const SAFE = false;

        function search($id){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);

            
            if ($conn->connect_error) {
                print("Es folgt fehler meldung vom connector : ");
                die("Connection failed: " . $conn->connect_error);
            } 
            

             // select query
             $sql = 'SELECT user_msg.Msg FROM user_msg WHERE User_ID = '. $id;

             #print($sql);

             if ($result = $conn->query($sql)) {
                $user_msg[] = [];
                while ($data = $result->fetch_assoc()) {
                    $user_msg[] = $data;
                }
                array_shift($user_msg);
                return $user_msg;
            }
            
        }

        function searchForProduct($productname){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
             // select query
             $sql = 'SELECT First_Name, Last_Name, DoB FROM user_info WHERE First_Name = "' . $productname. '";';
             if ($result = $conn->query($sql)) {
                $products[] = [];
                while ($data = $result->fetch_assoc()) {
                    $products[] = $data;
                }
                array_shift($products);
                return $products;
            }
        }

        function getUserNameWihtId($id){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            $sql = "SELECT First_Name FROM user_info WHERE User_ID = " . $id;
            if ($result = $conn->query($sql)) {
                $data = $result->fetch_assoc();
                return $data["First_Name"];
            }
        }

        function loginUser($name, $passwowrd){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
             // select query
             $sql = 'SELECT * FROM user_info WHERE First_Name = ' . "'" . $name . "'" . ' AND password = '. $passwowrd;
             if ($result = $conn->query($sql)) {
                $data = $result->fetch_assoc();
                return $data;
            }
        }


        #stuff for fancy button
        function updateQuantity($quantity, $name){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
             // select query
             $sql = 'UPDATE products SET Quantity = ' + $quantity + 'WHERE Product_name = '  + $name;
             print("Wir senden");
             print($sql);
             $conn->query($sql);
        }

        function getFirstProduct(){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
             // select query
             $sql = 'SELECT Product_name FROM products LIMIT 1;';

             print("Wir senden");
             print($sql);
             if ($result = $conn->query($sql)) {
                $data = $result->fetch_assoc();
                print("Data ! ");
                print($data);
                return $data;
            }
        }

        function samSearchForProduct($productname){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
             // select query
             $sql = 'SELECT Product_name, Price, Quantity FROM products WHERE product_name LIKE "%' . $productname. '%"';
             #Hammer%" UNION SELECT Product_name, Price, Quantity FROM products -- %"%";
               
             if ($result = $conn->query($sql)) {
                $products[] = [];
                while ($data = $result->fetch_assoc()) {
                    $products[] = $data;
                }
                array_shift($products);
                return $products;
            }
        }

         /**
         * neues Product einfügen
         */
        function addItem($productname, $productprice) {
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            $sql = 'INSERT INTO products(Product_name, Price) VALUES("' . $productname . '",' .$productprice.')';
            $conn->query($sql);    
        } 

        function bulshit($string){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            $sql = "SELECT * FROM user_msg WHERE user_msg.Msg_ID = ". $string. ";"; #1 AND SLEEP(5)=0;
            $conn->query($sql);
        }


        function getUserNameFromId($id){
            $sql = 'SELECT user_login.Username FROM user_login WHERE user_login.User_ID = ?';
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            $stmt = $conn->prepare($sql); 
            $stmt->bind_param("i", $id);
            $stmt->execute();
            $result = $stmt->get_result()->fetch_assoc();
            //Das packen ins array ist dammit, falls mehree Elemente zurückkommen alles klappt

            return $result["Username"];
        }

        function getUserInfo($userName){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            $sql = "SELECT * FROM `user_info` WHERE user_info.First_Name = '". $userName. "'";
            if ($result = $conn->query($sql)) {
                $userInfo[] = [];
                while ($data = $result->fetch_assoc()) {
                    $userInfo[] = $data;
                }
                array_shift($userInfo);
                return $userInfo;
            }
        }

        #Register
        function add_user($username, $userlastname, $password) {
            // Verbindung zur Datenbank herstellen
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
          
            // Query vorbereiten, um Benutzer in die Datenbank hinzuzufügen
            $query = 'INSERT INTO user_info (First_name, Last_name, Passwort)
                      VALUES ("' . $username . '","' .$userlastname.'","' . $password .'")';
          
            // Query ausführen
            if (mysqli_query($conn, $query)) {
              return true;
            } else {
              return false;
            }
          
          }
          function getUser($firstName){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            $sql = 'SELECT * FROM user_info WHERE First_Name = ' . "'" . $firstName . "'";
            // select query
            if ($result = $conn->query($sql)) {
               $data = $result->fetch_assoc();
               return $data;
           }
          }
          

        /** 
         * Sichereheit durch prepared statment 
        */
        function saveSearch($id){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            $sql = 'SELECT * FROM user_msg WHERE User_ID = ?';
            $stmt = $conn->prepare($sql); 
            $stmt->bind_param("i", $id);
            $stmt->execute();
            $result = $stmt->get_result()->fetch_assoc();
            //Das packen ins array ist dammit, falls mehree Elemente zurückkommen alles klappt
            $return = [];
            $return[] = $result;

            return $return;
        }


        function validateLogin($userName, $password){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            $sql = "SELECT First_Name, password FROM user_info WHERE First_Name = '". $userName. "'";
            #$sql = "SELECT Username, User_Pass FROM user_login WHERE Username = '". $userName. "'";
            if ($result = $conn->query($sql)) {
                 $pass = $result->fetch_assoc();
            }
            if($pass != NULL){
                if ($pass["password"] == $password) return TRUE;}
            return FALSE;
            
        }
        #saveSamShop(SSS)
        function saveAddItem($productname, $productprice) {
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            if ($conn->connect_error) {
                print("Es folgt fehler meldung vom connector : ");
                die("Connection failed: " . $conn->connect_error);
            }
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            $sql = 'INSERT INTO products(Product_name, Price) VALUES(?,?)';
            $stmt = $conn->prepare($sql); 
            $stmt->bind_param("sd", $productname, $productprice);
            $stmt->execute();
        }
        function saveSearchForProduct($productname){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
            $sql = 'SELECT Product_name, Price, Quantity FROM products WHERE product_name LIKE ?';
            //$sql = 'SELECT Product_name, Price, Quantity FROM products WHERE product_name = ?';

         
            $stmt = $conn->prepare($sql); 
            $input = "%$productname%";
            $stmt->bind_param("s", $input);
            $stmt->execute();
         
            $return[] = [];
            $result = $stmt->get_result();
            while($data = $result->fetch_assoc()){
                $return[] = $data;
            }
            
            
            return $return;
            
        }
    }
?>