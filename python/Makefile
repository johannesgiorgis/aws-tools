name := "aws-tools-python:1.0"
args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

format:
	fd "py$$" | xargs black

build: 
	docker build --rm -t ${name} .
    # docker build --rm -t aws-tools-python:1.0 .

fresh-build:
	docker build --rm --no-cache -t ${name} .

# run:
    # docker run -it --rm aws-tools-python:1.0

show:
	@docker container run --rm -v "${PWD}":/app -v ${HOME}/.aws:/root/.aws ${name} ls -ltFA /app | grep "aws.\+py"

run:
	@echo ${args}
	# docker container run --rm -v "${PWD}":/app -v ${HOME}/.aws":/root/.aws ${name} python /app/${args}

all:
	echo ${name}
	echo $@

action:
	@echo action $(filter-out $@,$(MAKECMDGOALS))
	@echo ${args}

%:		# thanks to chakrit
	@:    # thanks to William Pursell