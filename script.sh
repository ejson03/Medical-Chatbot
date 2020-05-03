#!/bin/bash
secret=$(openssl rand -hex 12)
export SECRET_KEY=$secret
python3 /app/setup.py
