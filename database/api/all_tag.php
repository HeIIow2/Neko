<?php
$credentials = json_decode(file_get_contents("private/database.json"));

$servername = $credentials -> servername;
$username = $credentials -> username;
$password = $credentials -> password;
$dbname = $credentials -> dbname;

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

function get_rand_row($result) {
	$rowcount = mysqli_num_rows($result);
	$n = rand(1, $rowcount);
	$row;
	for ($i=0;$i<$n;$i++) {
		$row = $result -> fetch_assoc();
	}
	return $row;
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
		$row['tags'] = get_img_tags($img_id);
		return $row;
	}
}


$sql = "SELECT DISTINCT tag.*,
COUNT(tag.id) AS frequency
FROM tag
LEFT OUTER JOIN image_tag ON tag.id=image_tag.tag_id
GROUP BY tag.id
ORDER BY frequency DESC;";
if(isset($_GET['frequency'])) 
{
	$sql = "SELECT * FROM tag;";
}
$result = select($sql);
if($result == NULL) {not_found();}
	
$tags = [];

for ($i=0; $i<$result->num_rows; $i++)
{
	 array_push($tags, $result -> fetch_assoc());
}

echo json_encode($tags);
die();
