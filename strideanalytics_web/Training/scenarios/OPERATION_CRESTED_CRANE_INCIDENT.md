# INCIDENT SCENARIO: OPERATION CRESTED CRANE
### Central Bank Payment Settlement Breach & Forensic Investigation Drill

---

## 🏛️ Context & Threat Profile
- **Target Organization:** Bank of Uganda (BoU), National Payment Systems & RTGS Division
- **Threat Actor:** *FIN-UG7 (State-Sponsored Financial Cybercrime Syndicate)*
- **Objective:** Illicit diversion of UGX 4.8 Billion via unauthorized batch injection into the interbank RTGS queue, followed by log wiping and domain extortion.

---

## ⏱️ Attack Timeline (Chronological Telemetry)

### Phase 1: Initial Access (T-0 to T+2 hrs)
- **Vector:** Exploitation of an unpatched SSL-VPN concentrator allocated to a third-party core banking maintenance vendor (`vendor_fintech_vpn`).
- **Artifact:** Ingress IP `194.26.29.11` logs into internal gateway `10.12.4.15` using stolen credentials without active hardware 2FA.

### Phase 2: Internal Reconnaissance & Privilege Escalation (T+2 to T+6 hrs)
- **Actions:** 
  - Attacker executes `whoami /priv` and discovers `SeDebugPrivilege`.
  - Memory extraction of LSASS process dumps domain administrator NTLM hashes.
  - Creation of a stealth scheduled task: `Microsoft\Windows\CustomerExperience\SvcUpdate` executing a base64 encoded Cobalt Strike beacon.

### Phase 3: The Target — RTGS Batch Injection (T+6 to T+7 hrs)
- **Actions:**
  - Injection of a memory patch into the RTGS transaction signing service (`bou_rtgs_service.exe`, PID 4128) bypassing dual-authorization enforcement.
  - An unauthorized batch wire is queued: **UGX 4,800,000,000** targeted at beneficiary account `CR-8831-EXT`.
  - Attempted log wiping via `wevtutil cl Security` (detected and blocked by Centralized Syslog immutability).

### Phase 4: SOC Detection & Containment (T+7 hrs)
- BoU Tier-2 SOC observes anomalous out-of-hours wire authorization and isolates host `BOU-RTGS-SRV01` from the core payment VLAN.
- Incident Commander invokes **BoU CSIRT Escalation Level 1** and deploys forensic acquisition protocols.

---

## 🎯 Masterclass Participant Objectives across the 5 Days
1. **Day 1**: Acquire bitstream logs and establish legally defensible cryptographic integrity.
2. **Day 2**: Trace the attacker's network C2 traffic, beacon timing, and unmask the staging IP.
3. **Day 3**: Extract volatile memory from `PID 4128` to isolate the injected memory patch.
4. **Day 4**: Contain the compromised domain accounts, reset Kerberos `krbtgt`, and construct YARA rules.
5. **Day 5**: Compile the Executive Incident Dossier and present testimony under the Uganda Computer Misuse Act.
