#!/usr/bin/env bash
echo "Starting Vercel Build Process..."
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput --clear
echo "Vercel Build Completed Successfully!"
