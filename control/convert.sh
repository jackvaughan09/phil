#!/bin/bash
for file in ($1).{doc,docx} ; do
    # antiword "$file" > "${file%.doc}.pdf"
    # for some reason (and I'm inexperienced in bash), calling on antiword first helps unoconv...
    $2 $3 "$file";
done;

