all: install check config test

install:
ifneq ($(shell id -u), 0)
	@echo "You are not root, \"make install\" should be run as root"
	exit 1
endif
	apt update
	apt install -y python2.7
ifeq (,$(shell ls /usr/bin/ | grep -w "python"$))
	ln -s /usr/bin/python2.7 /usr/bin/python
endif
	apt install -y wget
ifeq (,$(shell ls | grep get-pip))
	wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
endif
	python get-pip.py
	pip2 install -r requirements.txt
	apt install -y python-tk
	make -f MakeSniper

config:
ifeq (,$(shell ls MultiExplorer/src/ | grep config.py))
	cp MultiExplorer/src/config.example.py MultiExplorer/src/config.py
else
	@echo "MultiExplorer/src/config.py already found, make sure it's properly set."
endif
ifeq (,$(shell ls | grep -w "\.env"))
	cp example.env .env
else
	@echo ".env already found, make sure it's properly set."
endif

test:
	python ME.py

python2-check:
ifeq (,$(shell which python2))
	@printf 'python2 \xE2\x9C\x95\n'
else
	@printf 'python2 \xE2\x9C\x93\n'
endif

pip2-check:
ifeq (,$(shell which pip2))
	@printf 'pip2 \xE2\x9C\x95\n'
else
	@printf 'pip2 \xE2\x9C\x93\n'
endif

lxml-check:
ifeq (,$(shell pip2 freeze 2>/dev/null | grep lxml))
	@printf 'lxml \xE2\x9C\x95\n'
else
	@printf 'lxml \xE2\x9C\x93\n'
endif

configparser-check:
ifeq (,$(shell pip2 freeze 2>/dev/null | grep configparser))
	@printf 'configparser \xE2\x9C\x95\n'
else
	@printf 'configparser \xE2\x9C\x93\n'
endif

scikit-check:
ifeq (,$(shell pip2 freeze 2>/dev/null| grep scikit-learn==0.19.1))
	@printf 'scikit-learn==0.19.1 \xE2\x9C\x95\n'
else
	@printf 'scikit-learn 0.19.1\xE2\x9C\x93\n'
endif

check:python2-check pip2-check lxml-check configparser-check scikit-check
