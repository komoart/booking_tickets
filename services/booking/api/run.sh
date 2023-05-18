#!/bin/sh
cd src && gunicorn --bind 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornH11Worker main:app