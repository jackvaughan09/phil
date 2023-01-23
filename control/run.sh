#! bin/bash
source venv/bin/activate
which python
which unoconv
which soffice
which base
which pyuno
pyuno --version
unoconv --version
soffice --version
python clean.py ../data/zip ../data/unzipped
./convert.sh  ../data/unzipped
python mksheet.py ../data/unzipped