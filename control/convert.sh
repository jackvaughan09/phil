#!/bin/bash
cd $1
for file in *.doc ; do
    # antiword "$file" > "${file%.doc}.pdf"
    # for some reason (and I'm inexperienced in bash), calling on antiword first helps unoconv...
    unoconv "$file";
done;

