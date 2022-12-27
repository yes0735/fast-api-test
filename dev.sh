#!/bin/sh
#python ./main.py

# docker compose up
uvicorn app.main:app --reload
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker app.main:app --reload