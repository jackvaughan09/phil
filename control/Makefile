# abstraction of variables to circumvent OS incompatibilities within Makefile, no containerization needed
ifeq ($(OS),Windows_NT)
	VENV = venv\Scripts
	FILE = Activate.bat
	ACTIVATE = $(VENV)\$(FILE)
	PIP = $(VENV)\pip
	RM = del /S /F /Q 1>nul
	RM_MISC = echo "No miscellaneous files to delete in Windows"
	UNZIPPED = ..\data\unzipped\*
	PYTHON = $(VENV)\python
	OFFICE_PYTHON = "C:\Program Files (x86)\LibreOffice 4.4\program\python.exe"
	UNOCONV = $(VENV)\unoconv
# MAKESHELL = \bin\sh
else # linux/macos 
	VENV ?= venv/bin
	FILE ?= activate
	ACTIVATE ?= . $(VENV)/$(FILE)
	PIP ?= $(VENV)/pip
	RM ?= rm -rf
	RM_MISC ?= find .. -name .DS_Store -type f -delete
	UNZIPPED = ../data/unzipped/*
	PYTHON = $(VENV)/python
	UNOCONV = $(VENV)/unoconv
    OFFICE_PYTHON = /usr/bin/python3.8
endif                      #usr/bin/libreoffice

test all:
	$(warning $(UNO_PATH) $(origin UNO_PATH))

setup: requirements.txt
# docker build -t phil .
	python3 -m venv venv
	$(ACTIVATE)
	$(PIP) install -r requirements.txt
	$(ACTIVATE)
	$(PIP) install -r requirements.txt
	
run: $(ACTIVATE)
	$(PYTHON) clean.py
	bash convert.sh  $(UNZIPPED) $(OFFICE_PYTHON) $(UNOCONV)
	$(PYTHON) mksheet.py ../data/unzipped

# consider using the wsl python path?
# consider using the venv python path?

clean:
	@echo $(RM)
	$(RM) $(UNZIPPED)
	$(RM) *.pyc
	$(RM_MISC)