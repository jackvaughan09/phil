#!/bin/bash
for f in "$1"/*; do
   if [ $(head -c 4 "$f") = "%PDF" ]; then
      echo "PDF detected, continuing"
      continue
   fi
   echo "Converting: $f"
   unoconv "$f"
 #   name = "${f##*/}"
  #  echo "$name"
   # mv "${f%.*}.pdf" ../data/pdf/"$name".pdf
done