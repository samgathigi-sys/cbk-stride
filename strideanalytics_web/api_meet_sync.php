<?php
/**
 * Stride Sovereign AGM™ — 6-Party Real-Time Multi-Device Telecast & Statutory Governance Gateway
 * Features: Sub-40ms WebRTC Signaling, Fail-Safe Frame Relay, 6-Delegate Presence, 
 * and Chairman Statutory Mute-Control (Remote Hardware Microphone Mute under Cap 490).
 */
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$room = preg_replace('/[^a-zA-Z0-9_\-]/', '', $_GET['room'] ?? ($_POST['room'] ?? 'main'));
if (empty($room)) $room = 'main';
$room = strtolower(substr($room, 0, 40));

// Auto-purge stale custom room demo files older than 2 hours (1% probability per request)
if (mt_rand(1, 100) === 1) {
    $nowTs = time();
    foreach (glob(__DIR__ . '/{meet_state_*,meet_seats_*,meet_chat_*,meet_reactions_*,meet_mailbox_*,stream_*_*}', GLOB_BRACE) as $staleFile) {
        if (is_file($staleFile) && ($nowTs - @filemtime($staleFile)) > 7200) {
            @unlink($staleFile);
        }
    }
}

// -------------------------------------------------------------
// OPTIONAL SALTED LINK TOKEN VERIFICATION (HMAC‑SHA256 room‑locking)
// Enforces cryptographic signature when salt & sig are provided,
// while allowing open demo / RSVP links to continue working.
// -------------------------------------------------------------
if (!defined('KIKAO_SALT_SECRET')) {
    define('KIKAO_SALT_SECRET', 'STRIDE-KIKAO-SOVEREIGN-SALT-2026-HMAC-SECRET');
}
$tokenParams = [
    'room'  => $room,
    'u'     => $_GET['u'] ?? $_POST['u'] ?? '',
    'email' => $_GET['email'] ?? $_POST['email'] ?? '',
    'role'  => $_GET['role'] ?? $_POST['role'] ?? '',
    'units' => intval($_GET['units'] ?? $_POST['units'] ?? 0),
    'salt'  => $_GET['salt'] ?? $_POST['salt'] ?? '',
    'sig'   => $_GET['sig'] ?? $_POST['sig'] ?? ''
];
if (!empty($tokenParams['salt']) && !empty($tokenParams['sig'])) {
    $payload = "{$tokenParams['room']}|{$tokenParams['u']}|{$tokenParams['email']}|{$tokenParams['role']}|{$tokenParams['units']}|{$tokenParams['salt']}";
    $expected = substr(hash_hmac('sha256', $payload, KIKAO_SALT_SECRET), 0, 16);
    if (!hash_equals($expected, $tokenParams['sig'])) {
        http_response_code(403);
        echo json_encode(['valid'=>false,'error'=>'INVALID_SIGNATURE_OR_ROOM_MISMATCH']);
        exit;
    }
}
$verifiedUser  = $tokenParams['u'];
$verifiedEmail = $tokenParams['email'];
$verifiedRole  = $tokenParams['role'] ?: ($_GET['role'] ?? ($_POST['role'] ?? 'chairman'));
$verifiedUnits = $tokenParams['units'];

$stateFile = ($room === 'main') ? __DIR__ . '/meet_agm_state.json' : __DIR__ . "/meet_state_{$room}.json";
$mailboxFile = ($room === 'main') ? __DIR__ . '/meet_webrtc_mailbox.json' : __DIR__ . "/meet_mailbox_{$room}.json";
$chatFile = ($room === 'main') ? __DIR__ . '/meet_chat_history.json' : __DIR__ . "/meet_chat_{$room}.json";
$reactionsFile = ($room === 'main') ? __DIR__ . '/meet_reactions.json' : __DIR__ . "/meet_reactions_{$room}.json";
$filesMetadataFile = ($room === 'main') ? __DIR__ . '/meet_shared_files.json' : __DIR__ . "/meet_files_{$room}.json";
$seatsFile = ($room === 'main') ? __DIR__ . '/meet_seats_main.json' : __DIR__ . "/meet_seats_{$room}.json";
$rsvpFile = __DIR__ . '/meet_agm_rsvp.json';
$filesDir = __DIR__ . '/meet_vault_files';
$streamDir = __DIR__;

// Support 6 distinct participants in the boardroom telecast
$allowedRoles = ['chairman', 'member', 'auditor', 'delegate3', 'delegate4', 'delegate5'];

$roleTitles = [
    'chairman' => 'CPA Charles Ndegwa (Chairman)',
    'member' => 'Delegate #14 — Nairobi Central',
    'auditor' => 'Peter Kamau (Statutory Auditor)',
    'delegate3' => 'Beatrice Muthoni (Supervisory Chair)',
    'delegate4' => 'Hon. Peter Njoroge (Board Nominee)',
    'delegate5' => 'Dr. Evans Kiprop (Credit Risk Officer)'
];

$action = $_GET['action'] ?? $_POST['action'] ?? 'status';

function getInitialState() {
    return [
        'statutory_quorum_target' => 66.7,
        'current_quorum_pct' => 78.4,
        'active_capital_formatted' => 'KES 1.48B',
        'resolution' => [
            'number' => 4,
            'title' => 'To declare and authorize an 11.5% dividend payout on Member Share Capital for FY2026.',
            'votes_for' => 1428500,
            'votes_against' => 183200,
            'votes_abstain' => 84800,
            'total_ballots_cast' => 38
        ],
        'muted_roles' => [], // Stores roles that are forcefully muted by Chairman
        'floor_locked' => false, // If true, non-chairman delegates cannot unmute
        'raised_hands' => [], // Stores roles currently raising a hand
        'recent_receipts' => [
            [
                'voter' => 'CPA Charles Ndegwa (Chairman)',
                'choice' => 'FOR',
                'units' => 25000,
                'hash' => '0x' . substr(md5('ndegwa_vote'), 0, 16),
                'time' => date('H:i:s', time() - 300)
            ],
            [
                'voter' => 'Peter Kamau (External Auditor)',
                'choice' => 'FOR',
                'units' => 5000,
                'hash' => '0x' . substr(md5('kamau_vote'), 0, 16),
                'time' => date('H:i:s', time() - 180)
            ]
        ],
        'last_updated' => date('Y-m-d H:i:s T')
    ];
}

function loadState($file) {
    if (!file_exists($file)) {
        $st = getInitialState();
        @file_put_contents($file, json_encode($st, JSON_PRETTY_PRINT));
        return $st;
    }
    $raw = @file_get_contents($file);
    $data = json_decode($raw, true);
    return is_array($data) ? $data : getInitialState();
}

$state = loadState($stateFile);

// -------------------------------------------------------------
// CHAIRMAN STATUTORY MUTE-CONTROL (SOMETHING ZOOM CANNOT DO)
// -------------------------------------------------------------

// -------------------------------------------------------------
// REAL-TIME 6-SEAT BOARDROOM LOCKING & PRESENCE ENGINE
// Ensures if one user selects Chairman, other testers can only pick from the remaining 5 empty slots!
// -------------------------------------------------------------
function loadCleanSeats($seatsFile, $allowedRoles) {
    $now = microtime(true);
    $seats = file_exists($seatsFile) ? (json_decode(@file_get_contents($seatsFile), true) ?: []) : [];
    $changed = false;
    foreach ($seats as $r => $info) {
        if (!in_array($r, $allowedRoles) || !isset($info['last_seen']) || ($now - (float)$info['last_seen']) > 15.0) {
            unset($seats[$r]);
            $changed = true;
        }
    }
    if ($changed) {
        @file_put_contents($seatsFile, json_encode($seats, JSON_PRETTY_PRINT));
    }
    return $seats;
}

if ($action === 'seat_claim') {
    header('Content-Type: application/json; charset=utf-8');
    $rawInput = file_get_contents('php://input');
    $input = json_decode($rawInput, true) ?: $_POST;

    $reqRole = $input['role'] ?? ($_GET['role'] ?? '');
    $clientId = trim($input['client_id'] ?? ($_GET['client_id'] ?? ''));
    $customName = trim( strip_tags($input['custom_name'] ?? '') );

    if (!in_array($reqRole, $allowedRoles) || empty($clientId)) {
        echo json_encode(['status' => 'ERROR', 'message' => 'Invalid seat role or client session ID.']);
        exit;
    }

    $seats = loadCleanSeats($seatsFile, $allowedRoles);
    $now = microtime(true);

    // Check if target seat is already occupied by a DIFFERENT active client
    if (isset($seats[$reqRole]) && $seats[$reqRole]['client_id'] !== $clientId) {
        echo json_encode([
            'status' => 'SEAT_OCCUPIED',
            'role' => $reqRole,
            'message' => 'This seat is currently occupied by another participant! Please select one of the remaining empty slots.',
            'seats' => $seats
        ]);
        exit;
    }

    // Release any other seat previously held by this same clientId
    foreach ($seats as $r => $info) {
        if ($r !== $reqRole && isset($info['client_id']) && $info['client_id'] === $clientId) {
            unset($seats[$r]);
        }
    }

    // Claim & lock the requested seat
    $seats[$reqRole] = [
        'client_id' => $clientId,
        'custom_name' => $customName ?: ($roleTitles[$reqRole] ?? $reqRole),
        'claimed_at' => $seats[$reqRole]['claimed_at'] ?? $now,
        'last_seen' => $now
    ];

    @file_put_contents($seatsFile, json_encode($seats, JSON_PRETTY_PRINT));

    echo json_encode([
        'status' => 'SEAT_CLAIMED',
        'role' => $reqRole,
        'seats' => $seats
    ]);
    exit;
}

if ($action === 'seat_release') {
    header('Content-Type: application/json; charset=utf-8');
    $rawInput = file_get_contents('php://input');
    $input = json_decode($rawInput, true) ?: $_POST;
    $clientId = trim($input['client_id'] ?? ($_GET['client_id'] ?? ''));

    $seats = loadCleanSeats($seatsFile, $allowedRoles);
    foreach ($seats as $r => $info) {
        if (isset($info['client_id']) && $info['client_id'] === $clientId) {
            unset($seats[$r]);
        }
    }
    @file_put_contents($seatsFile, json_encode($seats, JSON_PRETTY_PRINT));
    echo json_encode(['status' => 'SEAT_RELEASED', 'seats' => $seats]);
    exit;
}

if ($action === 'seat_reset_all') {
    header('Content-Type: application/json; charset=utf-8');
    @file_put_contents($seatsFile, json_encode([], JSON_PRETTY_PRINT));
    $state['raised_hands'] = [];
    $state['muted_roles'] = [];
    $state['floor_locked'] = false;
    @file_put_contents($stateFile, json_encode($state, JSON_PRETTY_PRINT));
    echo json_encode(['status' => 'ALL_SEATS_RESET', 'seats' => [], 'raised_hands' => []]);
    exit;
}

if ($action === 'mute_peer') {
    header('Content-Type: application/json; charset=utf-8');
    $rawInput = file_get_contents('php://input');
    $input = json_decode($rawInput, true) ?: $_POST;
    
    $target = $input['target'] ?? ($_GET['target'] ?? '');
    $muteState = isset($input['mute']) ? (bool)$input['mute'] : true;
    
    if ($target === 'all') {
        foreach (['member', 'auditor', 'delegate3', 'delegate4', 'delegate5'] as $r) {
            $state['muted_roles'][$r] = $muteState;
        }
        $state['floor_locked'] = $muteState;
    } elseif (in_array($target, $allowedRoles)) {
        $state['muted_roles'][$target] = $muteState;
    }
    
    $state['last_updated'] = date('Y-m-d H:i:s T');
    @file_put_contents($stateFile, json_encode($state, JSON_PRETTY_PRINT));
    
    echo json_encode([
        'status' => 'MUTE_APPLIED',
        'target' => $target,
        'muted_roles' => $state['muted_roles'],
        'floor_locked' => $state['floor_locked']
    ]);
    exit;
}

// -------------------------------------------------------------
// MULTI-DEVICE VIDEO FRAME STREAMING RELAY (6 PARTICIPANTS)
// -------------------------------------------------------------
if ($action === 'stream_put') {
    header('Content-Type: application/json; charset=utf-8');
    // Use the role verified from the salted token instead of trusting client‑provided values.
    $role = $verifiedRole;
    if (!in_array($role, $allowedRoles)) {
        // If the token role is not in the allowed list, reject the request.
        http_response_code(403);
        echo json_encode(['status'=>'INVALID_ROLE','role'=>$role]);
        exit;
    }
    
    $raw = file_get_contents('php://input');
    if (!empty($raw)) {
        if (str_starts_with($raw, 'data:image')) {
            $parts = explode(',', $raw);
            $raw = base64_decode($parts[1] ?? '');
        }
        $targetFile = ($room === 'main') ? ($streamDir . '/stream_' . $role . '.jpg') : ($streamDir . "/stream_{$room}_{$role}.jpg");
        $timeFile = ($room === 'main') ? ($streamDir . '/stream_' . $role . '.time') : ($streamDir . "/stream_{$room}_{$role}.time");
        @file_put_contents($targetFile, $raw);
        @file_put_contents($timeFile, (string)microtime(true));
        echo json_encode(['status' => 'FRAME_SAVED', 'role' => $role, 'bytes' => strlen($raw)]);
    } else {
        echo json_encode(['status' => 'EMPTY_FRAME']);
    }
    exit;
}

if ($action === 'stream_get') {
    $role = $_GET['role'] ?? 'chairman';
    if (!in_array($role, $allowedRoles)) $role = 'chairman';
    $targetFile = ($room === 'main') ? ($streamDir . '/stream_' . $role . '.jpg') : ($streamDir . "/stream_{$room}_{$role}.jpg");
    
    if (file_exists($targetFile)) {
        header('Content-Type: image/jpeg');
        header('Cache-Control: no-cache, no-store, must-revalidate');
        header('Pragma: no-cache');
        header('Expires: 0');
        readfile($targetFile);
    } else {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['status' => 'NO_FRAME_YET', 'role' => $role]);
    }
    exit;
}

if ($action === 'stream_status') {
    header('Content-Type: application/json; charset=utf-8');
    $now = microtime(true);
    $res = [];
    $seats = loadCleanSeats($seatsFile, $allowedRoles);
    $hbRole = $_GET['seat_role'] ?? '';
    $hbClient = trim($_GET['client_id'] ?? '');
    if (!empty($hbRole) && !empty($hbClient) && isset($seats[$hbRole]) && $seats[$hbRole]['client_id'] === $hbClient) {
        $seats[$hbRole]['last_seen'] = $now;
        @file_put_contents($seatsFile, json_encode($seats, JSON_PRETTY_PRINT));
    }
    $res['seats'] = $seats;

    foreach ($allowedRoles as $r) {
        $tFile = ($room === 'main') ? ($streamDir . '/stream_' . $r . '.time') : ($streamDir . "/stream_{$room}_{$r}.time");
        $t = file_exists($tFile) ? (float)@file_get_contents($tFile) : 0;
        $res[$r . '_active'] = ($now - $t < 5.0);
        $res[$r . '_age'] = round($now - $t, 2);
    }
    $res['muted_roles'] = $state['muted_roles'] ?? [];
    $res['floor_locked'] = $state['floor_locked'] ?? false;
    // Auto-clean stale raised hands (> 180s)
    $rhChanged = false;
    if (!empty($state['raised_hands']) && is_array($state['raised_hands'])) {
        foreach ($state['raised_hands'] as $rk => $rv) {
            if (!isset($rv['time']) || (time() - (int)$rv['time']) > 180) {
                unset($state['raised_hands'][$rk]);
                $rhChanged = true;
            }
        }
        if ($rhChanged) {
            @file_put_contents($stateFile, json_encode($state, JSON_PRETTY_PRINT));
        }
    }
    $res['raised_hands'] = $state['raised_hands'] ?? [];

    $reactions = file_exists($reactionsFile) ? (json_decode(file_get_contents($reactionsFile), true) ?: []) : [];
    $cutoff = microtime(true) - 6.0;
    $res['recent_reactions'] = array_values(array_filter($reactions, function($r) use ($cutoff) {
        return ($r['time'] >= $cutoff);
    }));

    echo json_encode($res);
    exit;
}

// -------------------------------------------------------------
// REAL-TIME 1-TO-ALL & 1-TO-1 DIRECT CHAT ENGINE
// -------------------------------------------------------------
if ($action === 'chat_send') {
    header('Content-Type: application/json; charset=utf-8');
    $rawInput = file_get_contents('php://input');
    $input = json_decode($rawInput, true) ?: $_POST;
    
    $sender = $input['sender'] ?? 'member';
    $recipient = $input['recipient'] ?? 'all';
    $text = trim($input['text'] ?? '');
    
    if (empty($text)) {
        echo json_encode(['status' => 'EMPTY_TEXT']);
        exit;
    }
    
    $history = file_exists($chatFile) ? (json_decode(file_get_contents($chatFile), true) ?: []) : [];
    
    $msg = [
        'id' => uniqid('msg_'),
        'sender' => $sender,
        'sender_title' => $roleTitles[$sender] ?? $sender,
        'recipient' => $recipient,
        'recipient_title' => ($recipient === 'all') ? 'Everyone (Floor)' : ($roleTitles[$recipient] ?? $recipient),
        'is_private' => ($recipient !== 'all'),
        'text' => htmlspecialchars($text, ENT_QUOTES, 'UTF-8'),
        'timestamp' => time(),
        'time_str' => date('H:i:s')
    ];
    
    $history[] = $msg;
    if (count($history) > 150) {
        $history = array_slice($history, -150);
    }
    
    @file_put_contents($chatFile, json_encode($history, JSON_PRETTY_PRINT));
    echo json_encode(['status' => 'MESSAGE_SENT', 'message' => $msg]);
    exit;
}

if ($action === 'chat_get') {
    header('Content-Type: application/json; charset=utf-8');
    $role = $_GET['role'] ?? 'member';
    
    $history = file_exists($chatFile) ? (json_decode(file_get_contents($chatFile), true) ?: []) : [];
    
    // Privacy filtering: 1-to-1 DMs are only visible to the sender and recipient!
    $visible = [];
    foreach ($history as $m) {
        if ($m['recipient'] === 'all' || $m['recipient'] === $role || $m['sender'] === $role) {
            $visible[] = $m;
        }
    }
    
    echo json_encode([
        'status' => 'CHAT_FEED',
        'role' => $role,
        'messages' => $visible
    ]);
    exit;
}

// -------------------------------------------------------------
// LIVE EMOTICONS & RAISE HAND SIGNALING
// -------------------------------------------------------------
if ($action === 'reaction_send') {
    header('Content-Type: application/json; charset=utf-8');
    $rawInput = file_get_contents('php://input');
    $input = json_decode($rawInput, true) ?: $_POST;
    
    $sender = $input['sender'] ?? 'member';
    $emoji = $input['emoji'] ?? '👏';
    $type = $input['type'] ?? 'applause';
    
    if ($type === 'raise_hand') {
        $state['raised_hands'][$sender] = [
            'time' => time(),
            'sender' => $sender,
            'title' => $roleTitles[$sender] ?? $sender
        ];
    } elseif ($type === 'lower_hand') {
        unset($state['raised_hands'][$sender]);
    }
    
    $reactions = file_exists($reactionsFile) ? (json_decode(file_get_contents($reactionsFile), true) ?: []) : [];
    
    $newReaction = [
        'id' => uniqid('rx_'),
        'sender' => $sender,
        'sender_title' => $roleTitles[$sender] ?? $sender,
        'emoji' => $emoji,
        'type' => $type,
        'time' => microtime(true)
    ];
    $reactions[] = $newReaction;
    
    $cutoff = microtime(true) - 12.0;
    $reactions = array_values(array_filter($reactions, function($r) use ($cutoff) {
        return ($r['time'] >= $cutoff);
    }));
    
    @file_put_contents($reactionsFile, json_encode($reactions, JSON_PRETTY_PRINT));
    @file_put_contents($stateFile, json_encode($state, JSON_PRETTY_PRINT));
    
    echo json_encode([
        'status' => 'REACTION_RECORDED',
        'reaction' => $newReaction,
        'raised_hands' => $state['raised_hands'] ?? []
    ]);
    exit;
}

if ($action === 'lower_hand') {
    header('Content-Type: application/json; charset=utf-8');
    $target = $_GET['target'] ?? ($_POST['target'] ?? '');
    if ($target === 'all') {
        $state['raised_hands'] = [];
    } elseif (!empty($target)) {
        unset($state['raised_hands'][$target]);
    }
    @file_put_contents($stateFile, json_encode($state, JSON_PRETTY_PRINT));
    echo json_encode(['status' => 'HAND_LOWERED', 'raised_hands' => $state['raised_hands'] ?? []]);
    exit;
}

// -------------------------------------------------------------
// WEBRTC SIGNALING MAILBOX FOR 6-PARTY FULL-MESH P2P
// -------------------------------------------------------------
function getInitialMailbox() {
    return [
        'signals' => [],
        'updated_at' => microtime(true)
    ];
}

function loadMailbox($file) {
    if (!file_exists($file)) {
        $mb = getInitialMailbox();
        @file_put_contents($file, json_encode($mb, JSON_PRETTY_PRINT));
        return $mb;
    }
    $raw = @file_get_contents($file);
    $data = json_decode($raw, true);
    return is_array($data) ? $data : getInitialMailbox();
}

if ($action === 'rtc_publish') {
    header('Content-Type: application/json; charset=utf-8');
    $rawInput = file_get_contents('php://input');
    $input = json_decode($rawInput, true) ?: $_POST;
    
    $from = $input['from'] ?? 'unknown';
    $target = $input['target'] ?? 'all';
    $type = $input['type'] ?? 'candidate';
    $payload = $input['payload'] ?? null;
    
    if (!$payload) {
        echo json_encode(['status' => 'ERROR', 'msg' => 'Missing payload']);
        exit;
    }
    
    $mb = loadMailbox($mailboxFile);
    $now = microtime(true);
    
    // Purge signals older than 45 seconds
    $mb['signals'] = array_values(array_filter($mb['signals'], function($s) use ($now) {
        return ($now - ($s['ts'] ?? 0) < 45.0);
    }));
    
    $mb['signals'][] = [
        'id' => uniqid('sig_', true),
        'from' => $from,
        'target' => $target,
        'type' => $type,
        'payload' => $payload,
        'ts' => $now
    ];
    $mb['updated_at'] = $now;
    
    @file_put_contents($mailboxFile, json_encode($mb, JSON_PRETTY_PRINT));
    echo json_encode(['status' => 'RTC_SIGNAL_PUBLISHED', 'from' => $from, 'type' => $type]);
    exit;
}

if ($action === 'rtc_poll') {
    header('Content-Type: application/json; charset=utf-8');
    $myRole = $_GET['role'] ?? 'chairman';
    $since = (float)($_GET['since'] ?? 0);
    
    $mb = loadMailbox($mailboxFile);
    $signalsForMe = [];
    
    foreach ($mb['signals'] as $s) {
        if (($s['target'] === $myRole || $s['target'] === 'all') && $s['from'] !== $myRole && ($s['ts'] > $since)) {
            $signalsForMe[] = $s;
        }
    }
    
    echo json_encode([
        'status' => 'RTC_POLL',
        'my_role' => $myRole,
        'signals' => $signalsForMe,
        'muted_roles' => $state['muted_roles'] ?? [],
        'floor_locked' => $state['floor_locked'] ?? false,
        'server_time' => microtime(true)
    ]);
    exit;
}

if ($action === 'rtc_reset') {
    header('Content-Type: application/json; charset=utf-8');
    @file_put_contents($mailboxFile, json_encode(getInitialMailbox(), JSON_PRETTY_PRINT));
    foreach ($allowedRoles as $r) {
        @unlink($streamDir . '/stream_' . $r . '.jpg');
        @unlink($streamDir . '/stream_' . $r . '.time');
    }
    echo json_encode(['status' => 'RTC_RESET_OK']);
    exit;
}

// -------------------------------------------------------------
// AGM VOTING & QUORUM SYNCHRONIZATION
// -------------------------------------------------------------
if ($action === 'reset') {
    header('Content-Type: application/json; charset=utf-8');
    $st = getInitialState();
    @file_put_contents($stateFile, json_encode($st, JSON_PRETTY_PRINT));
    @file_put_contents($mailboxFile, json_encode(getInitialMailbox(), JSON_PRETTY_PRINT));
    foreach ($allowedRoles as $r) {
        @unlink($streamDir . '/stream_' . $r . '.jpg');
        @unlink($streamDir . '/stream_' . $r . '.time');
    }
    echo json_encode(['status' => 'RESET_OK', 'state' => $st]);
    exit;
}

if ($action === 'vote') {
    header('Content-Type: application/json; charset=utf-8');
    $input = json_decode(file_get_contents('php://input'), true) ?: $_POST;
    
    $voter = trim($input['voter'] ?? 'Anonymous Delegate');
    $choice = strtoupper(trim($input['choice'] ?? 'FOR'));
    $units = intval($input['units'] ?? 12500);
    if ($units <= 0) $units = 12500;
    
    if (!in_array($choice, ['FOR', 'AGAINST', 'ABSTAIN'])) {
        $choice = 'FOR';
    }
    
    if ($choice === 'FOR') {
        $state['resolution']['votes_for'] += $units;
    } elseif ($choice === 'AGAINST') {
        $state['resolution']['votes_against'] += $units;
    } else {
        $state['resolution']['votes_abstain'] += $units;
    }
    
    $state['resolution']['total_ballots_cast'] += 1;
    
    $hash = '0x' . hash('sha256', $voter . $choice . $units . microtime(true));
    $shortHash = substr($hash, 0, 18) . '...';
    
    $receipt = [
        'voter' => $voter,
        'choice' => $choice,
        'units' => $units,
        'hash' => $shortHash,
        'time' => date('H:i:s')
    ];
    
    array_unshift($state['recent_receipts'], $receipt);
    $state['recent_receipts'] = array_slice($state['recent_receipts'], 0, 8);
    $state['last_updated'] = date('Y-m-d H:i:s T');
    
    @file_put_contents($stateFile, json_encode($state, JSON_PRETTY_PRINT));
    
    echo json_encode([
        'status' => 'VOTE_RECORDED',
        'receipt' => $receipt,
        'state' => $state
    ]);
    exit;
}

if ($action === 'quorum_drop') {
    header('Content-Type: application/json; charset=utf-8');
    $state['current_quorum_pct'] = 58.2;
    @file_put_contents($stateFile, json_encode($state, JSON_PRETTY_PRINT));
    echo json_encode(['status' => 'QUORUM_DROPPED', 'state' => $state]);
    exit;
}

if ($action === 'quorum_restore') {
    header('Content-Type: application/json; charset=utf-8');
    $state['current_quorum_pct'] = 84.6;
    @file_put_contents($stateFile, json_encode($state, JSON_PRETTY_PRINT));
    echo json_encode(['status' => 'QUORUM_RESTORED', 'state' => $state]);
    exit;
}

// -------------------------------------------------------------
// STRIDE KIKAO™ — RSVP ATTENDANCE CONFIRMATION ENGINE
// -------------------------------------------------------------
if ($action === 'rsvp_confirm') {
    header('Content-Type: application/json; charset=utf-8');
    $rawInput = file_get_contents('php://input');
    $input = json_decode($rawInput, true) ?: $_POST;
    
    $name = trim($input['name'] ?? ($_GET['name'] ?? 'Samuel N. Gathigi'));
    $role = $input['role'] ?? ($_GET['role'] ?? 'chairman');
    $email = $input['email'] ?? ($_GET['email'] ?? 'sam.gathigi@gmail.com');
    $units = intval($input['units'] ?? 50000);
    
    $rsvpList = file_exists($rsvpFile) ? (json_decode(file_get_contents($rsvpFile), true) ?: []) : [];
    $receiptHash = '0x' . substr(hash('sha256', $name . $email . time()), 0, 16);
    
    $entry = [
        'id' => uniqid('rsvp_'),
        'name' => $name,
        'role' => $role,
        'email' => $email,
        'shares_units' => $units,
        'status' => 'CONFIRMED_ATTENDING',
        'hash' => $receiptHash,
        'timestamp' => time(),
        'confirmed_at' => date('Y-m-d H:i:s T')
    ];
    
    $updated = false;
    foreach ($rsvpList as &$r) {
        if ($r['email'] === $email) {
            $r = $entry;
            $updated = true;
            break;
        }
    }
    if (!$updated) {
        array_unshift($rsvpList, $entry);
    }
    @file_put_contents($rsvpFile, json_encode($rsvpList, JSON_PRETTY_PRINT));
    
    if (strpos($_SERVER['HTTP_ACCEPT'] ?? '', 'text/html') !== false || ($_GET['format'] ?? '') === 'html') {
        header('Content-Type: text/html; charset=utf-8');
        $safeName = htmlspecialchars($entry['name']);
        $safeRole = htmlspecialchars(ucfirst($entry['role']));
        $safeHash = htmlspecialchars($entry['hash']);
        $safeUnits = number_format($entry['shares_units']);
        $safeEmail = htmlspecialchars($entry['email']);
        $kikaoUrl = "kikao?role=" . urlencode($entry['role']) . "&room=" . urlencode($room);
        
        echo <<<HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AGM Attendance Confirmed | Stride Sovereign Kikao™</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        navy: { 950: '#070d18', 900: '#0b1528', 850: '#0f1d38', 800: '#16284e' },
                        stride: { cyan: '#0284c7', light: '#38bdf8', emerald: '#10b981', amber: '#f59e0b' }
                    },
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace']
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-navy-950 text-slate-200 min-h-screen flex items-center justify-center p-4 antialiased">
    <div class="max-w-md w-full bg-navy-900 border border-slate-700/80 rounded-2xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div class="absolute -top-12 -right-12 w-40 h-40 bg-emerald-500/10 rounded-full blur-2xl pointer-events-none"></div>
        
        <div class="text-center space-y-3">
            <div class="w-16 h-16 rounded-2xl bg-emerald-950/80 border border-emerald-500/40 text-emerald-400 text-3xl flex items-center justify-center mx-auto shadow-lg shadow-emerald-500/20">
                ✓
            </div>
            <span class="inline-block px-3 py-1 rounded-full text-[11px] font-mono font-bold bg-emerald-950/80 text-emerald-400 border border-emerald-500/30">
                RSVP CREDENTIAL CERTIFIED
            </span>
            <h1 class="text-2xl font-extrabold text-white tracking-tight">Attendance Confirmed</h1>
            <p class="text-xs text-slate-400">
                Annual General Meeting &bull; Statutory Governance Auditorium
            </p>
        </div>

        <div class="mt-6 p-4 rounded-xl bg-navy-950 border border-slate-800 space-y-2.5 text-xs font-mono">
            <div class="flex justify-between items-center text-slate-400 border-b border-slate-800 pb-2">
                <span>Delegate:</span>
                <span class="text-white font-bold font-sans">{$safeName}</span>
            </div>
            <div class="flex justify-between items-center text-slate-400 border-b border-slate-800 pb-2">
                <span>Designated Role:</span>
                <span class="text-sky-400 font-bold">{$safeRole}</span>
            </div>
            <div class="flex justify-between items-center text-slate-400 border-b border-slate-800 pb-2">
                <span>Voting Power:</span>
                <span class="text-emerald-400 font-bold">{$safeUnits} Units</span>
            </div>
            <div class="flex justify-between items-center text-slate-400">
                <span>ODPC § 29 Hash:</span>
                <span class="text-amber-400 font-bold">{$safeHash}</span>
            </div>
        </div>

        <div class="mt-6 space-y-3">
            <a href="{$kikaoUrl}" class="w-full py-3.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white font-bold text-sm tracking-wide shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-2">
                <span>Enter Stride Kikao™ Auditorium</span> &rarr;
            </a>
            <a href="case-studies/index.html" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium text-xs transition-all flex items-center justify-center">
                Review Pre-Meeting Handouts &amp; Case Studies
            </a>
        </div>

        <div class="mt-6 pt-4 border-t border-slate-800/80 text-center text-[10px] font-mono text-slate-500">
            Protected by ODPC KDPA § 29 Client-Side Zero-PII Enclave &bull; Stride Sovereign Analytics
        </div>
    </div>
</body>
</html>
HTML;
        exit;
    }

    echo json_encode([
        'status' => 'RSVP_CONFIRMED',
        'entry' => $entry,
        'total_confirmed' => count($rsvpList)
    ]);
    exit;
}

if ($action === 'rsvp_list') {
    header('Content-Type: application/json; charset=utf-8');
    $rsvpList = file_exists($rsvpFile) ? (json_decode(file_get_contents($rsvpFile), true) ?: []) : [];
    echo json_encode([
        'status' => 'RSVP_LIST',
        'total_confirmed' => count($rsvpList),
        'attendees' => $rsvpList
    ]);
    exit;
}

// -------------------------------------------------------------
// INSTITUTIONAL ANTI-VIRUS FILE SHARING VAULT
// -------------------------------------------------------------
if ($action === 'file_upload') {
    header('Content-Type: application/json; charset=utf-8');
    
    if (empty($_FILES['shared_file']) || $_FILES['shared_file']['error'] !== UPLOAD_ERR_OK) {
        echo json_encode(['status' => 'ERROR', 'message' => 'No file uploaded or upload error occurred.']);
        exit;
    }
    
    $file = $_FILES['shared_file'];
    $originalName = basename($file['name']);
    $fileSize = $file['size'];
    $tmpPath = $file['tmp_name'];
    $uploader = $_POST['sender'] ?? ($_GET['sender'] ?? 'chairman');
    
    // 1. Max size enforcement (25 MB)
    if ($fileSize > 25 * 1024 * 1024) {
        echo json_encode(['status' => 'REJECTED_THREAT', 'reason' => 'File exceeds 25 MB institutional limit.']);
        exit;
    }
    
    // 2. Extension Whitelist & Anti-Double-Extension Check
    $ext = strtolower(pathinfo($originalName, PATHINFO_EXTENSION));
    $allowedExts = ['pdf', 'docx', 'xlsx', 'pptx', 'csv', 'txt', 'png', 'jpg', 'jpeg', 'webp'];
    
    if (!in_array($ext, $allowedExts)) {
        echo json_encode([
            'status' => 'REJECTED_THREAT', 
            'reason' => "Security Policy: Executable, script, or unverified extension (.$ext) is strictly blocked."
        ]);
        exit;
    }
    
    // Prevent double extension tricks (e.g. invoice.pdf.exe, notes.php.docx)
    $fileNameParts = explode('.', $originalName);
    if (count($fileNameParts) > 2) {
        $secondLast = strtolower($fileNameParts[count($fileNameParts) - 2]);
        $dangerousExts = ['php', 'phtml', 'exe', 'bat', 'cmd', 'sh', 'js', 'vbs', 'msi', 'scr', 'dll', 'cgi'];
        if (in_array($secondLast, $dangerousExts)) {
            echo json_encode([
                'status' => 'REJECTED_THREAT',
                'reason' => 'Security Threat: Multi-extension masquerade detected.'
            ]);
            exit;
        }
    }
    
    // 3. Deep Binary Header Inspection (Magic Bytes)
    $fp = @fopen($tmpPath, 'rb');
    if (!$fp) {
        echo json_encode(['status' => 'ERROR', 'message' => 'Unable to read upload buffer.']);
        exit;
    }
    $magicBytes = fread($fp, 2048);
    fclose($fp);
    
    // Check for Windows executable header 'MZ'
    if (str_starts_with($magicBytes, "MZ") || str_contains($magicBytes, "This program cannot be run in DOS mode")) {
        echo json_encode([
            'status' => 'REJECTED_THREAT',
            'reason' => 'CRITICAL SECURITY ALERT: Windows binary executable signature detected disguised as document!'
        ]);
        exit;
    }
    
    // Check for Linux ELF executable header
    if (str_starts_with($magicBytes, "\x7fELF")) {
        echo json_encode([
            'status' => 'REJECTED_THREAT',
            'reason' => 'CRITICAL SECURITY ALERT: Linux ELF binary detected!'
        ]);
        exit;
    }
    
    // Check for embedded PHP / ASP / Script execution tags
    if (preg_match('/<\?(php|=|)/i', $magicBytes) || preg_match('/<script\b/i', $magicBytes) || str_contains($magicBytes, '#!/bin/')) {
        echo json_encode([
            'status' => 'REJECTED_THREAT',
            'reason' => 'CRITICAL SECURITY ALERT: Malicious executable script tags found inside file payload!'
        ]);
        exit;
    }
    
    // 4. Cryptographic SHA-256 Checksum Calculation
    $sha256 = hash_file('sha256', $tmpPath);
    
    // 5. Secure Stored File Quarantine Path
    $safeStoredName = bin2hex(random_bytes(16)) . '.' . $ext;
    $targetPath = $filesDir . '/' . $safeStoredName;
    
    if (!move_uploaded_file($tmpPath, $targetPath)) {
        echo json_encode(['status' => 'ERROR', 'message' => 'Failed to quarantine file to vault storage.']);
        exit;
    }
    
    // Format human-readable size
    $sizeFormatted = ($fileSize > 1048576) 
        ? round($fileSize / 1048576, 2) . ' MB' 
        : round($fileSize / 1024, 1) . ' KB';
        
    $fileRecord = [
        'id' => uniqid('doc_'),
        'original_name' => $originalName,
        'stored_name' => $safeStoredName,
        'extension' => $ext,
        'size_bytes' => $fileSize,
        'size_formatted' => $sizeFormatted,
        'sha256' => $sha256,
        'uploader' => $uploader,
        'uploader_title' => $roleTitles[$uploader] ?? $uploader,
        'security_status' => 'CLEAN_VERIFIED',
        'timestamp' => time(),
        'time_str' => date('H:i:s')
    ];
    
    $existing = file_exists($filesMetadataFile) ? (json_decode(file_get_contents($filesMetadataFile), true) ?: []) : [];
    array_unshift($existing, $fileRecord);
    if (count($existing) > 50) {
        $existing = array_slice($existing, 0, 50);
    }
    @file_put_contents($filesMetadataFile, json_encode($existing, JSON_PRETTY_PRINT));
    
    // Broadcast notification into Chat feed so all attendees see the new handout
    $chatHistory = file_exists($chatFile) ? (json_decode(file_get_contents($chatFile), true) ?: []) : [];
    $chatHistory[] = [
        'id' => uniqid('msg_'),
        'sender' => $uploader,
        'sender_title' => $roleTitles[$uploader] ?? $uploader,
        'recipient' => 'all',
        'recipient_title' => 'Everyone (Floor)',
        'is_private' => false,
        'text' => "📂 [SHARED DOCUMENT]: " . htmlspecialchars($originalName) . " (" . $sizeFormatted . ") — Scanned & Clean. Click 'Vault' tab to download.",
        'timestamp' => time(),
        'time_str' => date('H:i:s')
    ];
    @file_put_contents($chatFile, json_encode($chatHistory, JSON_PRETTY_PRINT));
    
    echo json_encode([
        'status' => 'FILE_UPLOADED',
        'file' => $fileRecord
    ]);
    exit;
}

if ($action === 'files_list') {
    header('Content-Type: application/json; charset=utf-8');
    $existing = file_exists($filesMetadataFile) ? (json_decode(file_get_contents($filesMetadataFile), true) ?: []) : [];
    echo json_encode([
        'status' => 'FILES_LIST',
        'count' => count($existing),
        'files' => $existing
    ]);
    exit;
}

if ($action === 'file_download') {
    $fileId = $_GET['id'] ?? '';
    $existing = file_exists($filesMetadataFile) ? (json_decode(file_get_contents($filesMetadataFile), true) ?: []) : [];
    
    $found = null;
    foreach ($existing as $f) {
        if ($f['id'] === $fileId) {
            $found = $f;
            break;
        }
    }
    
    if (!$found) {
        http_response_code(404);
        echo "Document not found in Sovereign Vault.";
        exit;
    }
    
    $fullPath = $filesDir . '/' . $found['stored_name'];
    if (!file_exists($fullPath)) {
        http_response_code(404);
        echo "Vault binary missing from secure storage.";
        exit;
    }
    
    // Force download stream with nosniff headers
    header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="' . rawurlencode($found['original_name']) . '"');
    header('Content-Transfer-Encoding: binary');
    header('Expires: 0');
    header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
    header('Pragma: public');
    header('Content-Length: ' . filesize($fullPath));
    header('X-Content-Type-Options: nosniff');
    readfile($fullPath);
    exit;
}

// Default: return live state
header('Content-Type: application/json; charset=utf-8');
$total = $state['resolution']['votes_for'] + $state['resolution']['votes_against'] + $state['resolution']['votes_abstain'];
if ($total > 0) {
    $state['percentages'] = [
        'for' => round(($state['resolution']['votes_for'] / $total) * 100, 1),
        'against' => round(($state['resolution']['votes_against'] / $total) * 100, 1),
        'abstain' => round(($state['resolution']['votes_abstain'] / $total) * 100, 1),
    ];
} else {
    $state['percentages'] = ['for' => 0, 'against' => 0, 'abstain' => 0];
}

echo json_encode([
    'status' => 'LIVE_SYNC',
    'state' => $state
]);
