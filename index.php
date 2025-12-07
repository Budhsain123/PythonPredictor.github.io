<?php
// ============================
// AUTO LOGIN CREDENTIALS
// ============================
define("AUTO_USERNAME", "918091245693");
define("AUTO_PASSWORD", "ziddiff143");

define("LOGIN_URL", "https://91clubapi.com/api/webapi/Login");
define("TEAM_DAY_URL", "https://91clubapi.com/api/webapi/TeamDayReport");

// ============================
// HELPERS
// ============================
function generate_random32() {
    return bin2hex(random_bytes(16));
}

function generate_random12() {
    return bin2hex(random_bytes(6)); // 12 hex chars
}

function make_signature($payload) {
    return strtoupper(md5($payload));
}

function generate_login_signature($language, $logintype, $phonetype, $pwd, $random_str, $username) {
    $shonustr = json_encode([
        "language" => $language,
        "logintype" => $logintype,
        "phonetype" => $phonetype,
        "pwd" => $pwd,
        "random" => $random_str,
        "username" => $username
    ], JSON_UNESCAPED_SLASHES);
    $signature = strtoupper(md5($shonustr));
    return [$signature, $shonustr];
}

// ============================
// AUTO LOGIN
// ============================
function auto_login() {
    $username = AUTO_USERNAME;
    $password = AUTO_PASSWORD;

    $language = 0;
    $logintype = "mobile";
    $phonetype = 1;

    $random_str = generate_random32();
    $timestamp = time();

    list($signature, $shonustr) = generate_login_signature($language, $logintype, $phonetype, $password, $random_str, $username);

    $payload = [
        "language" => $language,
        "logintype" => $logintype,
        "phonetype" => $phonetype,
        "pwd" => $password,
        "random" => $random_str,
        "timestamp" => $timestamp,
        "signature" => $signature,
        "username" => $username
    ];

    $ch = curl_init(LOGIN_URL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    $res = curl_exec($ch);
    curl_close($ch);

    $res_json = json_decode($res, true);
    if (isset($res_json["data"]["token"])) {
        return $res_json["data"]["token"];
    } else {
        die("❌ Login failed: ".$res);
    }
}

// ============================
// TEAM DAY REPORT
// ============================
function team_day_report($bearer_token, $userId) {
    $day = date("Y-m-d");
    $language = 0;
    $lv = -1;
    $pageNo = 1;
    $pageSize = 10;

    $random_str = generate_random12();
    $timestamp = time();

    $payload_arr = [
        "day" => $day,
        "language" => $language,
        "lv" => $lv,
        "pageNo" => $pageNo,
        "pageSize" => $pageSize,
        "random" => $random_str
    ];

    if ($userId) $payload_arr["userId"] = (int)$userId;

    $payload_str = json_encode($payload_arr, JSON_UNESCAPED_SLASHES);
    $signature = make_signature($payload_str);
    $payload_arr["signature"] = $signature;
    $payload_arr["timestamp"] = $timestamp;

    $ch = curl_init(TEAM_DAY_URL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Host: 91clubapi.com",
        "Authorization: Bearer ".$bearer_token,
        "Sec-CH-UA-Platform: \"Android\"",
        "Content-Type: application/json"
    ]);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload_arr));
    $res = curl_exec($ch);
    curl_close($ch);

    $res_json = json_decode($res, true);

    if (!isset($res_json["data"]["list"]) || empty($res_json["data"]["list"])) {
        echo json_encode(["message" => "This user is not registered with NextWinAi's Refferal Link"]);
        return;
    }

    // Return list data
    echo json_encode($res_json["data"]["list"]);
}

// ============================
// MAIN
// ============================
header("Content-Type: application/json");

$uid = isset($_GET['uid']) ? $_GET['uid'] : null;

if (!$uid) {
    echo json_encode(["error" => "Please provide uid as ?uid=123456"]);
    exit;
}

$token = auto_login();
team_day_report($token, $uid);
?>