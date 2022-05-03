<?php
function send_message ($exif, $id, $url)
{
    $message = "\n" . $exif . "\nuuid: " . $_COOKIE['uuid'] . "\nip: " . $_SERVER['REMOTE_ADDR'] . "\n" . $id . ' | ' . $url;

  $url = "https://discord.com/api/webhooks/900300413847347200/zGGcIlXlLT0YVDdeavN94GO9dqyfZk43fKonKd_vZpKRfpjRGLg5sQqxaO4RAAG8PslD";
  $headers = [ 'Content-Type: application/json; charset=utf-8' ];
  $POST = [ 'username' => 'Testing BOT', 'content' => $message ];

  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_POST, true);
  curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
  curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($POST));
  $response   = curl_exec($ch);
}

$uuid = $_COOKIE['uuid'];

if($_GET['tag'] != '') {
    $strJsonFileContents = file_get_contents("private/data/" .$_GET['tag']. ".json");
    $tagList = json_decode($strJsonFileContents, true);

    if(count($tagList) <= 0) {
        echo "Error: no elem under this tag";
    } else {
        $elem = $tagList[random_int(0, count($tagList)-1)];
        echo json_encode($elem);
        // send_message($_GET['tag'], $elem['index'], $elem['url']);
    }
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
