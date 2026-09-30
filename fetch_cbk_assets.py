import urllib.request
import re
import os

url = 'https://www.centralbank.go.ke'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        imgs = re.findall(r'src=["\']([^"\']+\.(?:png|svg|jpg|jpeg))["\']', html, re.I)
        print("Found images:", len(imgs))
        for img in imgs:
            if any(k in img.lower() for k in ['logo', 'cbk', 'crest', 'coat', 'bank']):
                print("Candidate:", img)
except Exception as e:
    print("Error:", e)
