# Day 2: Cyber Attack Vectors, Indicators of Compromise (IoCs) & Network Forensics

## 📌 Executive Agenda
- **09:00 - 10:30**: Attack Taxonomy in Banking: BEC, Banking Trojans, Ransomware & Core Banking Manipulations
- **10:45 - 12:30**: Threat Intelligence & Indicators of Compromise (IoCs): Hashes, IPs, Domains, JA3/JA4 Fingerprints
- **13:30 - 15:00**: Network Protocol Telemetry & Packet Inspection (Wireshark, Zeek, Suricata, NetFlow)
- **15:15 - 16:30**: **Lab 2**: Dissecting Financial Protocol Traffic, C2 Beacon Triage & Detecting Data Exfiltration

---

## 1. Banking Threat Vectors
1. **Business Email Compromise (BEC)**: Fraudulent wire instruction diversion targeting high-value RTGS settlements.
2. **Command & Control (C2) Channels**: DNS tunneling, domain fronting, HTTPS encrypted beacons masquerading as cloud telemetry.
3. **Lateral Movement & Credential Dumping**: Kerberoasting, Pass-the-Hash, and abuse of domain administrator tokens inside internal financial subnets.
4. **Supply Chain Compromise**: Backdoored banking software updates or third-party core banking integrator access.

---

## 2. Key Network Forensics Artifacts
- **Full Packet Capture (PCAP)**: Byte-for-byte record of transmission.
- **Protocol Metadata (Zeek)**: High-level connection, DNS, HTTP, SSL/TLS, and SSH logs without massive storage overhead.
- **NetFlow / IPFIX**: Flow volume, duration, source/destination IP/port metrics.
- **Firewall & Proxy Logs**: Ingress/egress drop events, user-agent anomalies, outbound payload size spikes.

---

## 3. Hands-On Lab 2: Network Telemetry & Suspicious Financial Wire Detection
See `labs/network_pcap_analyzer.py` for parsing packet traces and triaging suspicious outbound wire instructions and C2 beacon intervals.
