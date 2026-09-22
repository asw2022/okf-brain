#!/bin/bash
cd "/G/Download/OKF-Brain"
git add .
git commit -m "OKF backup $(date +%Y-%m-%d)" 2>/dev/null || echo "Nothing to commit"
git push origin master 2>/dev/null && echo "Backup OK" || echo "Push fehlgeschlagen"
