"""
CBK STRIDE - Robust Cloudflare Tunnel Supervisor
Writes output to disk log to prevent pipe buffer deadlocks.
Keeps CURRENT_LIVE_URL.txt synchronized with the active tunnel URL.
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import time
import re
import subprocess
import urllib.request
import ssl

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
URL_FILE = os.path.join(OUTPUT_DIR, "CURRENT_LIVE_URL.txt")
LOG_FILE = os.path.join(OUTPUT_DIR, "cloudflared.log")
CLOUDFLARED_EXE = os.path.join(OUTPUT_DIR, "cloudflared.exe")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def check_url(url):
    if not url:
        return False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (CBK-Supervisor)"})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            return resp.status == 200
    except Exception as e:
        return False

def start_tunnel():
    print("[SUPERVISOR] Launching cloudflared tunnel...")
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
        except Exception:
            pass

    log_handle = open(LOG_FILE, "w", encoding="utf-8")
    cmd = [CLOUDFLARED_EXE, "tunnel", "--url", "http://localhost:8501"]
    proc = subprocess.Popen(
        cmd,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )

    # Monitor log file for URL
    tunnel_url = None
    start = time.time()
    while time.time() - start < 30:
        time.sleep(1)
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                m = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", content)
                if m:
                    tunnel_url = m.group(0)
                    break

    if not tunnel_url:
        print("[SUPERVISOR] Failed to find tunnel URL in log.")
        try:
            proc.terminate()
        except Exception:
            pass
        return None, None, log_handle

    print(f"=======================================================")
    print(f"  ACTIVE LIVE URL: {tunnel_url}")
    print(f"=======================================================")

    with open(URL_FILE, "w", encoding="utf-8") as f:
        f.write(tunnel_url + "\n")

    return proc, tunnel_url, log_handle

def main():
    while True:
        proc, url, log_handle = start_tunnel()
        if not proc or not url:
            print("[SUPERVISOR] Retrying in 5 seconds...")
            time.sleep(5)
            continue

        consecutive_failures = 0
        while True:
            time.sleep(25)
            if proc.poll() is not None:
                print("[SUPERVISOR] Process exited. Restarting...")
                break

            healthy = check_url(url)
            if healthy:
                consecutive_failures = 0
                print(f"[SUPERVISOR] Tunnel health check OK: {url}")
            else:
                consecutive_failures += 1
                print(f"[SUPERVISOR] Tunnel health check FAILED ({consecutive_failures}/3): {url}")
                if consecutive_failures >= 3:
                    print("[SUPERVISOR] 3 consecutive failures. Restarting...")
                    try:
                        subprocess.run(["taskkill", "/f", "/t", "/pid", str(proc.pid)], capture_output=True)
                    except Exception:
                        pass
                    break

        try:
            log_handle.close()
        except Exception:
            pass
        time.sleep(3)

if __name__ == "__main__":
    main()
