VENV = venv/bin

run: $(VENV)/activate
	docker run -dp 3000:3000 phil
	$(VENV)/python3 clean.py 
	./convert.sh ../data/unzipped
	$(VENV)/python3 mksheet.py ../data/unzipped
setup: requirements.txt
	docker build -t phil .
	python3 -m venv venv
	. $(VENV)/activate
	$(VENV)/pip install -r requirements.txt
clean:
	rm -rf __pycache__
	rm -f ../data/unzipped/*
	rm -f *.pyc
	rm -f .DS_Store
	rm -f ../.DS_Store
	rm -f ../data/.DS_Store