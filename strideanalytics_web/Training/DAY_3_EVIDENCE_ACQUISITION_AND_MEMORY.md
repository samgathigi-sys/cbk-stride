# Day 3: Digital Evidence Acquisition, File Systems & Memory Forensics

## 📌 Executive Agenda
- **09:00 - 10:30**: Chain of Custody & Hardware Write-Blockers (ISO/IEC 27037 standards)
- **10:45 - 12:30**: Disk Imaging (Raw `dd`, E01 Expert Witness Format, AFF) & File System Analysis (NTFS MFT, EXT4 Inodes)
- **13:30 - 15:00**: Live Volatile Memory Forensics: Memory Acquisition (WinPmem, LiME) & Kernel Triage (Volatility 3)
- **15:15 - 16:30**: **Lab 3**: Reconstructing Deleted Transactions, Carving Data, and Extracting Injected DLLs from RAM

---

## 1. Physical vs. Logical vs. Bit-Stream Imaging
- **Physical Bit-Stream (Sector-by-Sector)**: Captures allocated clusters, unallocated space, slack space, and partition tables. Crucial for criminal and regulatory forensic evidence.
- **Hardware Write-Blockers**: Tableau / WiebeTech hardware write-blockers ensure no write signals reach the suspect storage medium.
- **Forensic Image Formats**:
  - `RAW / DD`: Direct uncompressed bitstream.
  - `E01 (EnCase / Expert Witness Format)`: Includes embedded metadata, acquisition notes, MD5/SHA-1 hashes, and internal CRC blocks.

---

## 2. Windows & Linux Banking Endpoint Artifacts
- **NTFS Master File Table ($MFT)**: File creation, modification, MFT change, and access timestamps ($STANDARD_INFORMATION vs $FILE_NAME timestamps for anti-forensic timestomping detection).
- **Windows Prefetch & Shimcache**: Evidence of execution showing executables launched by attackers even if deleted from disk.
- **Event Logs (EVTX)**: Security.evtx (Event ID 4624/4625 logons, 4688 process creation, 7045 new service installation).
- **RAM Artifacts**: Cleartext credentials (LSASS memory), active network sockets, decrypted TLS traffic, and injected payloads (`malfind`).

---

## 3. Hands-On Lab 3: Memory Triage with Volatility 3
```bash
# Example Volatility 3 workflow for a suspected banking terminal:
python vol.py -f memory.dmp windows.pslist
python vol.py -f memory.dmp windows.netscan
python vol.py -f memory.dmp windows.malfind
python vol.py -f memory.dmp windows.cmdline
```
