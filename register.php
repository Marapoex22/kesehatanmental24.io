<?php
// Koneksi ke database
$servername = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "uas";

$conn = new mysqli($servername, $dbusername, $dbpassword, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = password_hash($_POST["password"], PASSWORD_DEFAULT);

    $query = "INSERT INTO Users (username, password) VALUES (?, ?)";

    // Menyiapkan pernyataan
    if ($stmt = $conn->prepare($query)) {
        // Mengikat parameter
        $stmt->bind_param("ss", $username, $password);

        // Menjalankan pernyataan
        if ($stmt->execute()) {
            echo "Registration successful!";
        } else {
            echo "Error: " . $stmt->error;
        }

        // Menutup pernyataan
        $stmt->close();
    } else {
        echo "Error preparing statement: " . $conn->error;
    }
}

$conn->close();
?>
