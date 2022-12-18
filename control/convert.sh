#!/bin/bash
for file in "$1" ; do
$2 $3 "$file"
done