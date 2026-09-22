#!/bin/bash
cd "/G/Download/OKF-Brain"
git add .
git commit -m "OKF backup $(date +%Y-%m-%d)" 2>/dev/null || echo "Nothing to commit"
git push origin main 2>/dev/null || echo "Push failed - check remote"
