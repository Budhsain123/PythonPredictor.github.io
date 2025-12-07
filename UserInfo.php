<?php


error_reporting(0);


$AUTO_USERNAME = "918091245693";
$AUTO_PASSWORD = "ziddiff143";


$LOGIN_URL = "https://91clubapi.com/api/webapi/Login";
$TEAM_URL  = "https://91clubapi.com/api/webapi/TeamDayReport";



function random32() {
    return bin2hex(random_bytes(16));
}
function random12() {
    return bin2hex(random_bytes(16));
}


function login_signature($language, $logintype, $phonetype, $pwd, $random, $username) {
    $str = '{"language":'.$language.',"logintype":"'.$logintype.'","phonetype":'.$phonetype.',"pwd":"'.$pwd.'","random":"'.$random.'","username":"'.$username.'"}';
    return strtoupper(md5($str));
}



function auto_login($LOGIN_URL, $user, $pass) {

    $language = 0;
    $logintype = "mobile";
    $phonetype = 1;
    $random = random32();
    $timestamp = time();

    $sig = login_signature($language, $logintype, $phonetype, $pass, $random, $user);

    $payload = [
        "language" => $language,
        "logintype" => $logintype,
        "phonetype" => $phonetype,
        "pwd" => $pass,
        "random" => $random,
        "timestamp" => "$timestamp",
        "signature" => $sig,
        "username" => $user
    ];

    $ch = curl_init($LOGIN_URL);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $res = curl_exec($ch);
    curl_close($ch);

    $json = json_decode($res, true);

    if(isset($json["data"]["token"])) {
        return $json["data"]["token"];   
    }

    return null;
}



function team_day_report($TEAM_URL, $token, $uid) {

    $day = date("Y-m-d");
    $language = 0;
    $lv = -1;
    $pageNo = 1;
    $pageSize = 10;
    $random = random12();
    $timestamp = time();


    if($uid) {
        $payload_str = '{"day":"'.$day.'","language":'.$language.',"lv":'.$lv.',"pageNo":'.$pageNo.',"pageSize":'.$pageSize.',"random":"'.$random.'","userId":'.$uid.'}';
    } else {
        $payload_str = '{"day":"'.$day.'","language":'.$language.',"lv":'.$lv.',"pageNo":'.$pageNo.',"pageSize":'.$pageSize.',"random":"'.$random.'"}';
    }

    $signature = strtoupper(md5($payload_str));


    $body = [
        "day" => $day,
        "language" => $language,
        "lv" => $lv,
        "pageNo" => $pageNo,
        "pageSize" => $pageSize,
        "random" => $random,
        "signature" => $signature,
        "timestamp" => $timestamp
    ];
    if($uid) $body["userId"] = (int)$uid;

    $headers = [
        "Host: 91clubapi.com",
        "authorization: Bearer ".$token,
        "sec-ch-ua-platform: \"Android\"",
        "content-type: application/json"
    ];

    $ch = curl_init($TEAM_URL);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $res = curl_exec($ch);
    curl_close($ch);

    return json_decode($res, true);
}




$uid = isset($_GET["uid"]) ? $_GET["uid"] : "";

if(!$uid) {
    die("<b>Error:</b> Please use ?uid=USERID");
}


$token = auto_login($LOGIN_URL, $AUTO_USERNAME, $AUTO_PASSWORD);

if(!$token) {
    die("Login failed, unable to get token.");
}


$response = team_day_report($TEAM_URL, $token, $uid);


$list = $response["data"]["list"] ?? [];

if(count($list) == 0) {
    die("This user is not registered with NextWinAi's Referral Link");
}


$row = $list[0];

$nickname = $row["nickName"] ?? "";
$level    = $row["lv"] ?? "";


if($nickname == "" || $level == "" || $level == null) {
    die("This user is not registered with NextWinAi's Referral Link");
}


// ================= FINAL RESULT OUTPUT =================
echo "<pre>";
echo "UserID      : ".$row["userID"]."\n";
echo "Level       : ".$row["lv"]."\n";
echo "Recharge    : ".$row["rechargeAmount"]."\n";
echo "Rebate      : ".$row["rebateAmount"]."\n";
echo "Bet Amount  : ".$row["lotteryAmount"]."\n";
echo "Nick Name   : ".$row["nickName"]."\n";
echo "Search Time : ".$row["searchTime"]."\n";
echo "----------------------------------------\n";
echo "</pre>";
?>