import re

with open(r'C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\war_room_simulator.html', 'r', encoding='utf-8') as f:
    content = f.read()

js_calls = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", content)
html_ids = set(re.findall(r"id=['\"]([^'\"]+)['\"]", content))

missing = []
for cid in set(js_calls):
    if cid not in html_ids:
        missing.append(cid)

print("Missing IDs:", missing)
