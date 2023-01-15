# abstraction of variables to circumvent OS incompatibilities within Makefile, no containerization needed
ifeq ($(OS),Windows_NT)
	$(error Because you're running on Windows (are you using Windows Subsystem for Linux?) we may have trouble with convert.sh)
	VENV = venv\Scripts
	FILE = Activate.bat
	ACTIVATE = $(VENV)\$(FILE)
	PIP = $(VENV)\pip
	RM = del /S /F /Q 1>nul
	RM_MISC = echo "No miscellaneous files to delete in Windows"
	UNZIPPED = ..\data\unzipped\
	PYTHON = $(VENV)\python
	OFFICE_PYTHON = "C:\Program Files (x86)\LibreOffice 4.4\program\python.exe"
	UNOCONV = $(VENV)\unoconv
	PDF = ..\data\pdf\
# MAKESHELL = \bin\sh
else # linux/macos 
	VENV = venv/bin
	FILE = activate
	ACTIVATE = . $(VENV)/$(FILE)
	PIP = $(VENV)/pip
	RM = rm -rf
	RM_MISC = find .. -name .DS_Store -type f -delete
	UNZIPPED = ../data/unzipped
	PYTHON = $(VENV)/python
	UNOCONV = $(VENV)/unoconv
    OFFICE_PYTHON = /usr/bin/python3.10
	PDF = ../data/pdf
endif

setup: requirements.txt
	python3 -m venv venv
	echo $(ACTIVATE)
	$(ACTIVATE)
	$(PIP) install -r requirements.txt

clean:
	echo $(RM)
	$(RM) $(UNZIPPED)
	$(RM) $(PDF)m
	$(RM) *.pyc
	$(RM_MISC)

test: #$(ACTIVATE) clean
#	$(PYTHON) clean.py ../test_data/zip ../test_data/unzipped
#	./convert.sh ../test_data/unzipped
	$(PYTHON) test_extract_all.py

run: #$(ACTIVATE) test clean
#	$(PYTHON) clean.py ../data/zip ../data/unzipped
#	./convert.sh  $(UNZIPPED)
	$(PYTHON) mksheet.py ../data/unzipped