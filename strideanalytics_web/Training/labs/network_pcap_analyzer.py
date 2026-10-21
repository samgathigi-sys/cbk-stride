"""
Bank of Uganda Cyber Forensics Masterclass - Lab 2
Financial Threat Telemetry & Network Beacon Analyzer
Simulates packet inspection for anomalous C2 communications and unauthorized SWIFT/RTGS API calls.
"""

import math
import statistics
from datetime import datetime

class NetworkThreatAnalyzer:
    def __init__(self):
        self.suspect_ips = set()
        self.anomalous_sessions = []

    def analyze_beaconing(self, connection_intervals: list[float], jitter_threshold=0.15) -> dict:
        """
        Detect automated Command & Control (C2) beaconing via statistical regularity.
        Human-driven browsing exhibits high variance; automated bots exhibit low jitter.
        """
        if len(connection_intervals) < 5:
            return {"status": "INSUFFICIENT_DATA"}

        mean_interval = statistics.mean(connection_intervals)
        std_dev = statistics.stdev(connection_intervals)
        jitter = std_dev / mean_interval if mean_interval > 0 else 1.0

        is_c2_beacon = jitter < jitter_threshold

        return {
            "mean_interval_sec": round(mean_interval, 2),
            "std_deviation": round(std_dev, 2),
            "jitter_ratio": round(jitter, 4),
            "classification": "CONFIRMED_C2_BEACON" if is_c2_beacon else "ORGANIC_HUMAN_TRAFFIC",
            "threat_score": 90 if is_c2_beacon else 15
        }

    def inspect_financial_api_payload(self, payload: dict) -> dict:
        """Inspect outbound API / Webhook payload for anomalous wire transfer indicators."""
        flags = []
        amount = payload.get("amount", 0)
        currency = payload.get("currency", "UGX")
        dest_account = payload.get("dest_account", "")
        origin_ip = payload.get("origin_ip", "")

        # Flag 1: High value threshold check
        if currency == "UGX" and amount > 500_000_000:
            flags.append("HIGH_VALUE_TRANSACTION_EXCEEDING_STANDARD_LIMIT")
        elif currency == "USD" and amount > 150_000:
            flags.append("HIGH_VALUE_FX_TRANSFER")

        # Flag 2: Out of country or non-whitelisted routing IP
        if not origin_ip.startswith("10.") and not origin_ip.startswith("172.16."):
            flags.append("EXTERNAL_ORIGIN_IP_DIRECT_API_INJECTION")

        # Flag 3: Suspicious beneficiary formatting
        if len(dest_account) < 8 or dest_account.endswith("9999"):
            flags.append("HIGH_RISK_BENEFICIARY_ACCOUNT_PATTERN")

        return {
            "payload_id": payload.get("transaction_id"),
            "risk_level": "CRITICAL" if len(flags) >= 2 else ("ELEVATED" if flags else "NORMAL"),
            "detected_anomalies": flags,
            "action_recommended": "IMMEDIATE_REVOCATION_AND_FORENSIC_FREEZE" if len(flags) >= 2 else "ALLOW_WITH_LOGGING"
        }

def demo_network_lab():
    print("=" * 70)
    print("  BANK OF UGANDA CYBER FORENSICS LAB 2: NETWORK THREAT ANALYZER")
    print("=" * 70)

    analyzer = NetworkThreatAnalyzer()

    # Scenario A: Simulated Bot C2 Beacon (periodic heartbeat with slight noise)
    bot_traffic = [60.1, 59.8, 60.0, 60.2, 59.9, 60.3, 60.0, 59.7]
    result_bot = analyzer.analyze_beaconing(bot_traffic)
    print("\n[+] Telemetry Stream 1 (Suspect Host 10.12.8.44 -> 198.51.100.24):")
    print(f"    Mean Interval: {result_bot['mean_interval_sec']}s | Jitter: {result_bot['jitter_ratio']}")
    print(f"    Classification: {result_bot['classification']} (Threat Score: {result_bot['threat_score']}/100)")

    # Scenario B: Simulated Human Traffic
    human_traffic = [12.4, 45.1, 180.2, 5.3, 89.0, 240.5, 30.2]
    result_human = analyzer.analyze_beaconing(human_traffic)
    print("\n[+] Telemetry Stream 2 (User Workstation 10.12.8.112):")
    print(f"    Mean Interval: {result_human['mean_interval_sec']}s | Jitter: {result_human['jitter_ratio']}")
    print(f"    Classification: {result_human['classification']}")

    # Scenario C: Suspicious RTGS Outbound API Packet
    suspect_wire = {
        "transaction_id": "TX-2026-BOU-88914",
        "currency": "UGX",
        "amount": 1_850_000_000,
        "dest_account": "ACC-OFFSHORE-9999",
        "origin_ip": "194.26.29.11"
    }
    wire_audit = analyzer.inspect_financial_api_payload(suspect_wire)
    print("\n[+] Suspicious Wire Transfer API Inspection:")
    print(f"    Transaction ID: {wire_audit['payload_id']}")
    print(f"    Risk Level: {wire_audit['risk_level']}")
    print(f"    Anomalies Flagged: {wire_audit['detected_anomalies']}")
    print(f"    Recommendation: {wire_audit['action_recommended']}")

if __name__ == "__main__":
    demo_network_lab()
