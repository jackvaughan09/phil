#!/bin/bash
for f in "$1"/*; do
    unoconv "$f"
done