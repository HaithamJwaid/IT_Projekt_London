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
                while ($data = $result->fetch_assoc()) {
                    $user_msg[] = $data;
                }
                array_shift($user_msg);
                return $user_msg;
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
    }
?>