#!/bin/bash
for file in "$1" ; do
unoconv "$file"
done