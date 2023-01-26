#!/usr/bin/bash
for f in "$1"/*; do
	if [ "$(head -c 4 "$f")" = "%PDF" ]; then
		echo "PDF detected, continuing"
		mv "$f" ../data/pdf
		continue
	fi
	echo "Converting: $f"
	libreoffice --headless --convert-to pdf --outdir ../data/pdf "$f"
done
