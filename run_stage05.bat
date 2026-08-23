@echo off
title Stage 05: Asymmetric Acquisition Intelligence Terminal
echo =====================================================================
echo  Launching Stage 05: Mercedes-Benz Strategic Intelligence Terminal
echo  Access URL: http://localhost:8504
echo =====================================================================
cd /d "%~dp005-asymmetric-acquisition-mercedes-safeguards"
python -m streamlit run app.py --server.port 8504
pause
