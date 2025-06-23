#!/bin/bash
cd /home/ubuntu/Alyssa
source venv/bin/activate
cd app
exec uvicorn main:app --host 0.0.0.0 --port 3000
