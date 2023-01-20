# phil Setup Guide
Reduce the time requirement of audit report analysis.
## Instructions
### Installation

### Homebrew: (MacOS only)
If you don't already have it installed, visit this website https://brew.sh/ and follow the installation instructions. It's very straightforward. 
- Make sure you read the instructions printed in the terminal after installing homebrew in order to add to your system PATH. Important!! 


### WSL: (Windows only)
https://learn.microsoft.com/en-us/windows/wsl/install Follow this guide.

#### IMPORTANT INFORMATION

##### LibreOffice:
2. Now we install libreoffice


```bash
brew install libreoffice
```

3. Create a folder called Philipines in your Documents folder.  

4. Navigate to the folder in your terminal 
```bash
cd Documents/Philipines
```

5. Clone this repository
```bash
git clone https://github.com/hudnash/phil.git
```
- You may need to create a github account in order to clone the repository. If so, do that. 

6. While in the project's root directory (phil), run the following in your terminal:
```bash
cd control
```
#### Running make commands 
** Navigate to the phil/control directory.**
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
- If you experience any errors running 'source bin/activate', double check that you are in phil/control/venv

3. Navigate back to control & run make run: 
```bash
cd .. # <--move up from phil/control/venv to phil/control
make run 
```
4. Let the program run. The terminal will display "All done!" when it is finished.

5. Check the phil/data/xlsx folder. There should be a file with the user-provided filename.

6. (For testing features added to the project) To clean up the phil/data/unzipped folder for testing purposes prior to the next test, you may run:
```bash
make clean
```
### Running into problems?
7. When an audit region has an unbeforeseen format, submit an issue report in this GitHub repo and I will patch it.
8. If any issue occurs whatsoever, please submit an issue in this GitHub repo and I will handle it ASAP!!
