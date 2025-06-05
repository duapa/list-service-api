#!/bin/sh
. venv/bin/activate
exec uvicorn app.app:api --log-level=info --host 0.0.0.0 --port $PORT