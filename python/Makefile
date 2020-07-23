format:
	fd "py$$" | xargs black

build: 
    docker build --rm -t aws-tools-python:1.0 .

run:
    docker run -it --rm aws-tools-python:1.0