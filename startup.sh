#!/bin/bash

python pre_process.py
uvicorn app:app --host 0.0.0.0 --port 8000