#!/bin/bash
for f in "$1"/*; do
    unoconv "$f"
 #   name = "${f##*/}"
  #  echo "$name"
   # mv "${f%.*}.pdf" ../data/pdf/"$name".pdf

done