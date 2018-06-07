# Clean up the pycahe file and *.pyc file
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm {} +
	rm -rf project
	rm -rf home

create: 
	python3 manage.py startproject
	python3 manage.py startapp
