@echo off
title Stage 02: Toyota Hybrid Strategy Engine
echo Launching Stage 02 Simulator on Port 8501 (http://localhost:8501)...
cd /d "%~dp002-toyota-hybrid-multipathway-strategy"
python -m streamlit run dashboard/app.py --server.port 8501
pause
