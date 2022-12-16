# phil
Reduce the time requirement of audit report analysis.
## Instructions
### Installation
#### Installing Linux Distribution, LibreOffice, and the Phil repo
1. Install Cygwin on your Windows machine (if you are a Windows user). This makes me not need to finish debugging convert.bat (very difficult).
2. Install LibreOffice. If you have a Linux OS, simply run in the terminal:
```bash
sudo apt install libreoffice
```
- Make sure that your LibreOffice installation is located where control/Makefile thinks it is.
3. Clone this repository by running the following inside the src folder in your usr folder:
```bash
git clone https://github.com/hudnash/phil.git
```
4. While in the project's root directory (phil), run the following in your terminal:
```bash
cd phil/control
```
#### Running make commands
5. Navigate to the phil/control directory.
6. To create the virual environment and install the dependencies, run:
```bash
make setup
```
### Normal Operation: Transferring Audit Data to a Spreadsheet
1. Drop the .ZIP files in the phil/data/zip folder. Remove any .ZIP files that are unnecessary or that have already been scraped.
2. Run the following command in terminal:
```bash
cd phil/control
make run
```
3. Check the phil/data/xlsx folder. There should be a file with the user-provided filename.
4. (For testing features added to the project) To clean up the phil/data/unzipped folder for testing purposes prior to the next test, you may run:
```bash
make clean
```
### Running into problems?
5. When an audit region has an unbeforeseen format, submit an issue report in this GitHub repo and I will patch it.
6. If any issue occurs whatsoever, please submit an issue in this GitHub repo and I will handle it ASAP!!
