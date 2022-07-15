#!/bin/bash
cd $1
for file in *; do
	antiword "$file" > "${file%.*}.txt";
done;