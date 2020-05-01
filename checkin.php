<?php 

$usersJson = file_get_contents("users.json");
$userData = json_decode($usersJson, true);
foreach($userData as $user) {
    echo "<pre>";
    $username = $user['username'];
    $password = $user['password'];
    // $url = $topic['question_url'];
    if (!empty($username) && !empty($password)) {
        $command = "scrapy crawl checkin -s LOG_FILE=logs/checkin.log -a checktype=checkin -a username=".$username." -a password=".$password."";
        echo "<pre>";
        echo $command;
        echo "<pre>";
        echo 'Crawling.....';
        shell_exec($command);
        sleep(2);
    }

}
?>