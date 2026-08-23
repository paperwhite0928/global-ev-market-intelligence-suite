@echo off
title Stage 04: Geopolitical BCP Simulator
echo Launching Stage 04 BCP Engine on Port 8503 (http://localhost:8503)...
cd /d "%~dp004-mobility-geopolitical-bcp-engine"
python -m streamlit run app.py --server.port 8503
pause
