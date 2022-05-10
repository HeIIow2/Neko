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

function not_found()
{
	echo "404";
	http_response_code(404);
	die();
}

function get_tag_id_from_name($tag_name) {
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

function get_tag_name_from_id($tag_id) {
	$sql = "SELECT name FROM tag WHERE id='" . $tag_id . "';";
	$result = select($sql);
	
	if ($result == NULL) 
	{
		return NULL;
	} else 
	{
		$row = $result->fetch_assoc();
		return $row['name'];
	}
}

function get_rand_img_id_by_tag($tag_id) {
	GLOBAL $sfw;
	// get tag id
	$sql = "SELECT image_id AS id FROM image_tag 
			WHERE tag_id='" . $tag_id . "' 
			ORDER BY rand()
			LIMIT 1;";
	if ($sfw) {
		$sql = "SELECT DISTINCT image_id AS id FROM image_tag 
				WHERE tag_id=" . $tag_id . " AND image_id NOT IN 
				(SELECT DISTINCT image_id FROM image_tag 
				WHERE tag_id=8)
				ORDER BY rand()
				LIMIT 1;";
	}
	$result = select($sql);
	
	if ($result == NULL) 
	{
		return NULL;
	} else 
	{
		$row = $result -> fetch_assoc();
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

function get_img_data_by_id($img_id) {
	$sql = "SELECT * from image WHERE id=" . $img_id . ";";
	$result = select($sql);
	
	if ($result == NULL) 
	{
		return NULL;
	} else 
	{
		$row = $result -> fetch_assoc();
		// $row['tags'] = get_img_tags($img_id);
		return $row;
	}
}



if(isset($_GET['image_id'])) {
	$img_id = $conn->real_escape_string($_GET['image_id']);
	
	$img_data = get_img_data_by_id($img_id);
	if($img_data == NULL) {not_found();}
	
	echo json_encode($img_data);
	
	die();
}

if(isset($_GET['tag_id'])) 
{
	$tag_id = $conn->real_escape_string($_GET['tag_id']);
	
	$img_id = get_rand_img_id_by_tag($tag_id);
	if($img_id == NULL) {not_found();}
	
	$img_data = get_img_data_by_id($img_id);
	if($img_data == NULL) {not_found();}
	
	echo json_encode($img_data);
	die();
}

if(isset($_GET['tag_name']))
{
	$tag_name = $conn->real_escape_string($_GET['tag_name']);
	$tag_id = get_tag_id_from_name($tag_name);
	
	$img_id = get_rand_img_id_by_tag($tag_id);
	if($img_id == NULL) {not_found();}
	
	$img_data = get_img_data_by_id($img_id);
	if($img_data == NULL) {not_found();}
	
	echo json_encode($img_data);
	die();
}

