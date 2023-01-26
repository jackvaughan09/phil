#!/usr/bin/bash
venv/bin/python3 clean.py ../data/zip ../data/pdf
./convert.sh ../data/pdf
venv/bin/python3 mksheet.py ../data/pdf