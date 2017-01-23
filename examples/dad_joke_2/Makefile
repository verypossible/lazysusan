NAME = "joinspartan/serverless:1.4"

ENVDIR=envs
LIBS_DIR=Jokes2/lib


.PHONY:	libs shell env-dirs check-env tests deploy function

run = docker run --rm -it \
		-v `pwd`:/code \
		--env ENV=$(ENV) \
		--env-file envs/$2 \
		--name=jokes2-serverless-$(ENV) $(NAME) $1


all : build

build :
	docker build -t $(NAME) .

libs :
	@test -d $(LIBS_DIR) || mkdir -p $(LIBS_DIR)
	rm -rf $(LIBS_DIR)/*
	pip install -t $(LIBS_DIR) PyYAML
	@test -f $(LIBS_DIR)/_yaml.so && rm $(LIBS_DIR)/_yaml.so
	pip install -t $(LIBS_DIR) --no-deps -U git+https://github.com/spartansystems/lazysusan.git

shell : check-env env-dirs
	$(call run,bash,$(ENV))

env-dirs :
	@test -d $(ENVDIR)

tests : check-env
	$(call run,py.test tests,$(ENV))

# NOTE:
#
# 	Deployments assume you are already running inside the docker container
#
#
deploy : check-env
	cd Jokes2 && sls deploy -s $(ENV)

function : check-env
	cd Jokes2 && sls deploy -s $(ENV) function -f jokes2

# Note the ifndef must be unindented
check-env:
ifndef ENV
	$(error ENV is undefined)
endif
