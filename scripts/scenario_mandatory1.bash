#!/usr/bin/env bash
cd "../mandatory1/internal" || exit

# Start nemid_code_generator
cd "nemid_code_generator" || exit
uvicorn api:app --reload --port 8090
cd ".."

# Start nemid_password_generator
cd "nemid_password_generator" || exit
uvicorn api:app --reload --port 8089