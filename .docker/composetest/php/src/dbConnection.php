<?php

    class Connector{
        static $host = 'db';

        // Database use name
        static $user = 'root';

        //database user password
        static $pass = 'Darius1998';

        // database name
        static $mydatabase = 'MY_DATABASE';

        function search($id){
            $conn = new mysqli(Connector::$host, Connector::$user, Connector::$pass, Connector::$mydatabase);
             // select query
             $sql = 'SELECT * FROM user_msg WHERE User_ID = '. $id;
             if ($result = $conn->query($sql)) {
                $user_msg[] = [];
                while ($data = $result->fetch_object()) {
                    $user_msg[] = $data;
                }
                return $user_msg;
            }
        }
    }
?>