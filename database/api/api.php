<?php
$servername = "localhost";
$username = "Hellow2";
$password = "1234";
$dbname = "neko";

// Create connection to db
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
  die("Connection to database failed: " . $conn->connect_error);
}

$sfw = False;
if(isset($_GET['sfw'])) {
	$sfw = (bool)$_GET['sfw'];
}

function get_tag_id($tag_name) {
	GLOBAL $conn;
	// get tag id
	$sql = "SELECT id FROM tag WHERE name='" . $tag_name . "';";
	
	$result = $conn->query($sql);
	if ($result->num_rows > 0) {
		$result = $result->fetch_assoc();
		$tag_id = $result['id'];
		return $tag_id;
	} else {
		echo "404";
	}
}

function get_image_id_by_tag($tag_id) {
	GLOBAL $conn;
	// get tag id
	$sql = "SELECT id FROM tag WHERE name='" . $tag_name . "';";
	
	$result = $conn->query($sql);
	if ($result->num_rows > 0) {
		$result = $result->fetch_assoc();
		$tag_id = $result['id'];
		return $tag_id;
	} else {
		echo "404";
	}
}


if(isset($_GET['tag']) or isset($_GET['tag_name'])) {
	$tag_name;
	if($_GET['tag'] != '') {
		$tag_name = $_GET['tag'];
	} else {
		$tag_name = $_GET['tag_name'];
	}
	
	$tag_id = get_tag_id($tag_name);
	echo $tag_id;

        // $elem = $tagList[random_int(0, count($tagList)-1)];
        // echo json_encode($elem);
        // send_message($_GET['tag'], $elem['index'], $elem['url']);
    

} elseif ($_GET['download'] != '') {
    $strJsonFileContents = file_get_contents("private/table.json");
    $table = json_decode($strJsonFileContents, true);
    echo '<img src=' .json_encode($table[$_GET['download']]["url"]). '>';
    send_message("DOWNLOAD", $table[$_GET['download']]["index"], $table[$_GET['download']]["url"]);

} elseif($_GET['id'] != '') {
    $strJsonFileContents = file_get_contents("private/table.json");
    $table = json_decode($strJsonFileContents, true);
    echo json_encode($table[$_GET['id']]);
} else {
	echo "needs: tag, id or download";
}
