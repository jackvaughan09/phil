# phil
Minimize the time requirement of audit report analysis through consolidation, processing, and indicators.
## Instructions
1. Drop the .ZIP files in the phil/data/zip folder.
2. Run the following command in terminal:
```bash
cd phil/control
./convert.sh && python clean_dump_to_dir.py && python sheet.py
```
3. Check data/unzipped. There should be one of each .DOC, .TXT, and .PDF for each audit report in this folder, **assuming they are the same format as in Lamitan City 2010**.
4. Finally, check data/xlsx. This is where the tables should end up after being extracted.
5. When an audit region has an unbeforeseen format, submit an issue report in this GitHub repo and I will patch it.
6. If any issue occurs whatsoever, please submit an issue in this GitHub repo and I will handle it ASAP!!
