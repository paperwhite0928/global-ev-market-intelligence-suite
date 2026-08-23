@echo off
title Stage 03: BEV Econometric Platform
echo Launching Stage 03 Econometric Platform on Port 8502 (http://localhost:8502)...
cd /d "%~dp003-bev-adoption-drivers-econometrics"
python -m streamlit run ev_driver_analysis/app.py --server.port 8502
pause
