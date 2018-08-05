#!/bin/bash
gunicorn --bind 0.0.0.0:8080 core.wsgi 2>&1 | tee -a /logs/core$(date +%Y%m%d_%H%M%S).log
