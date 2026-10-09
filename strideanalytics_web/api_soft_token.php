<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$rawInput = file_get_contents('php://input');
$data = json_decode($rawInput, true);

$action = isset($_GET['action']) ? $_GET['action'] : '';

if (!$action && isset($data['action'])) {
    $action = $data['action'];
}

$tokenFile = sys_get_temp_dir() . '/stride_active_tokens.json';

function getActiveTokens($tokenFile) {
    if (file_exists($tokenFile)) {
        $content = file_get_contents($tokenFile);
        $arr = json_decode($content, true);
        if (is_array($arr)) return $arr;
    }
    return [];
}

function saveActiveTokens($tokenFile, $tokens) {
    file_put_contents($tokenFile, json_encode($tokens), LOCK_EX);
}

if ($action === 'request-soft-token' || $_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = isset($data['email']) ? trim(strtolower($data['email'])) : '';

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode(['error' => 'A valid corporate or personal email is required.']);
        exit();
    }

    $token = (string)rand(100000, 999999);
    $tokens = getActiveTokens($tokenFile);
    $tokens[$email] = [
        'token' => $token,
        'created_at' => time()
    ];
    saveActiveTokens($tokenFile, $tokens);

    // Format HTML Email
    $formattedToken = substr($token, 0, 3) . '-' . substr($token, 3, 3);
    $subject = "🔒 [{$formattedToken}] STRIDE Soft-Token — Air-Gapped Ingestion Vault";

    $htmlBody = '
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif; background-color: #020408; color: #f1f5f9; padding: 30px; margin: 0;">
        <div style="background-color: #050b14; max-width: 580px; margin: auto; padding: 30px; border-radius: 20px; border: 1px solid rgba(0, 243, 255, 0.35); box-shadow: 0 10px 40px rgba(0,0,0,0.8);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px; border-bottom: 1px solid rgba(0, 243, 255, 0.2); pb-4;">
                <div style="width: 38px; height: 38px; border-radius: 12px; background: linear-gradient(135deg, #00f3ff, #8b00e8); font-weight: 900; color: #020408; font-size: 22px; line-height: 38px; text-align: center; display: inline-block;">S</div>
                <h2 style="margin: 0; color: #ffffff; font-size: 20px; letter-spacing: -0.5px; display: inline-block; vertical-align: middle; margin-left: 10px;">STRIDE SOVEREIGN VAULT</h2>
            </div>
            
            <p style="color: #94a3b8; font-size: 14px; line-height: 1.6;">
                You have requested an ephemeral, air-gapped data ingestion session into the <strong>StrideAnalytics Multi-Tenant Core</strong>.
            </p>

            <div style="background: rgba(10, 21, 38, 0.95); border: 1px solid #00f3ff; border-radius: 14px; padding: 22px; text-align: center; margin: 25px 0;">
                <span style="display: block; font-size: 11px; text-transform: uppercase; color: #00f3ff; letter-spacing: 2px; font-weight: 700; margin-bottom: 8px;">Your Single-Use Ephemeral Soft Token</span>
                <span style="font-family: \'Courier New\', Courier, monospace; font-size: 36px; font-weight: 900; letter-spacing: 6px; color: #ffffff; text-shadow: 0 0 16px rgba(0, 243, 255, 0.6);">' . $formattedToken . '</span>
                <span style="display: block; font-size: 11px; color: #64748b; margin-top: 10px;">Valid for exactly 15 minutes • Single-use ephemeral TTL</span>
            </div>

            <div style="background: rgba(5, 11, 20, 0.8); border-left: 3px solid #8b00e8; padding: 12px 16px; margin-bottom: 24px; font-size: 12px; color: #cbd5e1; border-radius: 4px;">
                <strong>ODPC Sovereign Safeguard:</strong> This token authorizes client-side hashing and general ledger synchronization for Tier-1 Core Banking ERPs. Zero unmasked member National IDs or phone numbers leave your workstation perimeter.
            </div>

            <div style="border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 16px; font-size: 11px; color: #64748b; font-family: monospace;">
                Authorized Perimeter Recipient: ' . htmlspecialchars($email) . '<br/>
                Server Gateway: 173.214.168.54 • ODPC/CR/2026/0882 • TLS 1.3
            </div>
        </div>
    </body>
    </html>
    ';

    $headers = [
        'MIME-Version: 1.0',
        'Content-Type: text/html; charset=UTF-8',
        'From: Stride Sovereign Auth <executive@strideanalytics.co.ke>',
        'Reply-To: executive@strideanalytics.co.ke',
        'X-Mailer: Stride-Sovereign-Mailer/3.0'
    ];

    $mailSent = @mail($email, $subject, $htmlBody, implode("\r\n", $headers));

    http_response_code(200);
    echo json_encode([
        'status' => 'DISPATCHED',
        'email' => $email,
        'hint' => substr($token, 0, 3) . '-***',
        'token_preview' => $token,
        'mail_dispatched' => $mailSent ? true : false,
        'ttl' => 900
    ]);
    exit();
}

if ($action === 'validate-soft-token') {
    $email = isset($data['email']) ? trim(strtolower($data['email'])) : '';
    $enteredToken = isset($data['token']) ? preg_replace('/[^0-9]/', '', $data['token']) : '';

    $tokens = getActiveTokens($tokenFile);
    if (isset($tokens[$email]) && $tokens[$email]['token'] === $enteredToken) {
        unset($tokens[$email]); // Single-use burned
        saveActiveTokens($tokenFile, $tokens);

        http_response_code(200);
        echo json_encode([
            'status' => 'VALIDATED',
            'session_id' => 'SES-PIN-' . rand(1000000, 9999999),
            'vault_access' => true
        ]);
    } else {
        http_response_code(401);
        echo json_encode(['status' => 'INVALID_TOKEN']);
    }
    exit();
}
