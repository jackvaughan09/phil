# phil MacOS Setup
Reduce the time requirement of audit report analysis.
## Instructions
### Installation
#### Installing Homebrew and Libreoffice:

##### Homebrew:
1. If you don't already have it installed, visit this website https://brew.sh/ and follow the installation instructions. It's very straightforward. 
- Make sure you read the instructions printed in the terminal after installing homebrew in order to add to your system PATH. Important!! Then run:
```bash
brew install libreoffice
```
2. Create a folder called Philipines in your Documents folder.  
3. Navigate to the folder in your terminal 
```bash
cd Documents/Philipines
```
4. Clone this repository
```bash
git clone https://github.com/hudnash/phil.git
```
- You may need to create a github account in order to clone the repository. If so, do that. 
5. While in the project's root directory (phil), run the following in your terminal:
```bash
cd phil/control
```
#### Running make commands
6. Navigate to the phil/control directory.
7. To create the virual environment and install the dependencies, run:
```bash
make setup
```
### Normal Operation: Transferring Audit Data to a Spreadsheet
1. After downloading from the site, drop your .ZIP files in the phil/data/zip folder. Remove any .ZIP files that are unnecessary or that have already been scraped.
2. Run the following command in terminal:
```bash
cd phil/control/venv
source bin/activate
```
- This activates the virtual environment in which we run our code. You should see '(venv)' at the start of the current terminal line after running this.
3. Navigate back to control & run make run: (the 'cd ..' command moves you up one folder)
```bash
cd ..
make run
```
5. Check the phil/data/xlsx folder. There should be a file with the user-provided filename.
6. (For testing features added to the project) To clean up the phil/data/unzipped folder for testing purposes prior to the next test, you may run:
```bash
make clean
```
### Running into problems?
5. When an audit region has an unbeforeseen format, submit an issue report in this GitHub repo and I will patch it.
6. If any issue occurs whatsoever, please submit an issue in this GitHub repo and I will handle it ASAP!!
