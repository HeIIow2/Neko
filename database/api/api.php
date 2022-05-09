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

function select($sql) {
	GLOBAL $conn;
	$result = $conn->query($sql);

	if ($result->num_rows > 0) {
		return $result;
	} else {
		return NULL;
	}
}

function get_rand_row($result) 
{
	$rowcount = mysqli_num_rows($result);
	$n = rand(0, $rowcount);
	$row;
	for ($i=0;$i<$n;$i++) {
		$row = $result -> fetch_assoc();
	}
	return $row;
}

function get_tag_id($tag_name) {
	// get tag id
	$sql = "SELECT id FROM tag WHERE name='" . $tag_name . "';";
	$result = select($sql);
	
	if ($result == NULL) 
	{
		return NULL;
	} else 
	{
		$row = $result->fetch_assoc();
		return $row['id'];
	}


}


function get_rand_img_id_by_tag($tag_id) {
	GLOBAL $sfw;
	// get tag id
	$sql = "SELECT image_id AS id FROM image_tag 
			WHERE tag_id='" . $tag_id . "';";
	if ($sfw) {
		$sql = "SELECT DISTINCT image_id AS id FROM image_tag 
				WHERE tag_id=" . $tag_id . " AND image_id NOT IN 
				(SELECT DISTINCT image_id FROM image_tag 
				WHERE tag_id=8);";
	}
	$result = select($sql);
	
	if ($result == NULL) 
	{
		return NULL;
	} else 
	{
		$row = get_rand_row($result);
		return $row['id'];
	}
}

function get_img_tags($img_id) {
	$sql = "SELECT tag.name FROM tag 
			WHERE tag.id IN 
			(SELECT image_tag.tag_id FROM image_tag
			WHERE image_tag.image_id=" . $img_id . ");";
	$result = select($sql);
	
	if ($result == NULL) 
	{
		return NULL;
	} else 
	{
		$tags = [];
		while ($row = $result -> fetch_row()) {
			array_push($tags, $row[0]);
		}
		return $tags;
	}
}

function get_img_data($img_id) 
{
	$sql = "SELECT * from image WHERE id=" . $img_id . ";";
	$result = select($sql);
	
	if ($result == NULL) 
	{
		return NULL;
	} else 
	{
		$row = $result -> fetch_assoc();
		$row['tags'] = get_img_tags($img_id);
		return $row;
	}
}

$tag_name;
$tag_id;
$img_id;
$img_data;


if(isset($_GET['tag']) or isset($_GET['tag_name'])) {
	$tag_name;
	if($_GET['tag'] != '') {
		$tag_name = $_GET['tag'];
	} else {
		$tag_name = $_GET['tag_name'];
	}
	
	$tag_id = get_tag_id($tag_name);
	if ($tag_id == NULL) { 
		echo '404'; 
		die(); 
	}
	
	$img_id = get_rand_img_id_by_tag($tag_id);
	if ($img_id == NULL) { 
		echo '404'; 
		die(); 
	}
	
	$img_data = get_img_data($img_id);
	
	echo $json_img_data=json_encode($img_data);
}

if(isset($_GET['in'])) 
{
	if ($_GET['in'] == 'tag_name')
	{
		$tag_name = $_GET['tag_name'];
		
		$tag_id = get_tag_id($tag_name);
		if ($tag_id == NULL) { 
			echo '404'; 
			die(); 
		}
		echo $tag_id;
	}
}

if(isset($_GET['out']))
{
	if ($_GET['out'] == 'tag_id') {
		echo $tag_id;
	}
}

/*
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
}*/
