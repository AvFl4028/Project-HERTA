#!/bin/fish

set PYTHONPYCACHEPREFIX $(pwd)/__pycache__
# echo $PYTHONPYCACHEPREFIX
# python -X pycache_prefix="$(pwd)/__pycache__" src/main.py
uvicorn src.api.FastApi:app --reload
