<?php
session_start();
if (!isset($_SESSION["user_id"])) {
    header("Location: login.html");
    exit();
}

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "uas";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $user_id = $_SESSION["user_id"];
    
    $question1 = $_POST['question1'];
    $question2 = $_POST['question2'];
    $question3 = $_POST['question3'];
    $question4 = $_POST['question4'];
    $question5 = $_POST['question5'];
    $question6 = $_POST['question6'];
    $question7 = $_POST['question7'];
    $question8 = $_POST['question8'];
    
    $symptoms = "1: $question1, 2: $question2, 3: $question3, 4: $question4, 5: $question5, 6: $question6, 7: $question7, 8: $question8";

    $score = 0;
    $score += ($question1 == 'a') ? 1 : 0;
    $score += ($question2 == 'a') ? 1 : 0;
    $score += ($question3 == 'a') ? 1 : 0;
    $score += ($question4 == 'a') ? 1 : 0;
    $score += ($question5 == 'a') ? 1 : 0;
    $score += ($question6 == 'a') ? 1 : 0;
    $score += ($question7 == 'a') ? 1 : 0;
    $score += ($question8 == 'a') ? 1 : 0;

    if ($score >= 6) {
        $result = "Depresi berat";
    } elseif ($score >= 4) {
        $result = "Depresi sedang";
    } elseif ($score >= 2) {
        $result = "Depresi ringan";
    } else {
        $result = "Tidak ada depresi";
    }

    $sql = "INSERT INTO Diagnoses (user_id, symptom_ids, result) VALUES (?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("iss", $user_id, $symptoms, $result);

    if ($stmt->execute()) {
        echo "<div class='container mt-3'>";
        echo "<h2>Hasil Diagnosa</h2>";
        echo "<div class='alert alert-success'>$result</div>";
        echo "</div>";
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
    $conn->close();
}
?>
