#!/bin/sh
exec gunicorn -b :8001 --access-logfile - --error-logfile - app:app
