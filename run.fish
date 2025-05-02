#!/usr/bin/env fish
set pycache_dir (pwd)/__pycache__

python -X pycache_prefix=$pycache_dir -m uvicorn src.api.FastApi:app --reload

# python -X pycache_prefix="$(pwd)/__pycache__" src/main.py
# uvicorn src.api.FastApi:app --reload
