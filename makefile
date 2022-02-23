missing_deps := 0

all: check config test

install:
ifneq ($(shell id -u), 0)
	@echo "You are not root, \"make install\" should be run as root"
	exit 1
endif
	apt update
	apt install -y python2
	ln -s /usr/bin/python2 /usr/bin/python
	apt install -y wget
	wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
	python2 get-pip.py
	pip2 install -r requirements.txt

config:
ifeq (,$(shell ls MultiExplorer/src/ | grep config.py))
	cp MultiExplorer/src/config.example.py MultiExplorer/src/config.py
else
	@echo "MultiExplorer/src/config.py already found, make sure it's properly set."
endif

test:
	python MultiExplorer/src/MultiExplorer.py input-examples/quark.json

python2-check:
ifeq (,$(shell which python2))
	@printf 'python2 \xE2\x9C\x95\n'
missing_deps := 1
else
	@printf 'python2 \xE2\x9C\x93\n'
endif

pip2-check:
ifeq (,$(shell which pip2))
	@printf 'pip2 \xE2\x9C\x95\n'
missing_deps := 1
else
	@printf 'pip2 \xE2\x9C\x93\n'
endif

lxml-check:
ifeq (,$(shell pip2 freeze 2>/dev/null | grep lxml))
	@printf 'lxml \xE2\x9C\x95\n'
missing_deps := 1
else
	@printf 'lxml \xE2\x9C\x93\n'
endif

configparser-check:
ifeq (,$(shell pip2 freeze 2>/dev/null | grep configparser))
	@printf 'configparser \xE2\x9C\x95\n'
missing_deps := 1
else
	@printf 'configparser \xE2\x9C\x93\n'
endif

scikit-check:
ifeq (,$(shell pip2 freeze 2>/dev/null| grep scikit-learn==0.19.1))
	@printf 'scikit-learn==0.19.1 \xE2\x9C\x95\n'
missing_deps := 1
else
	@printf 'scikit-learn 0.19.1\xE2\x9C\x93\n'
endif

check:python2-check pip2-check lxml-check configparser-check scikit-check
ifeq ($(missing_deps), 1)
	@echo "There are missing dependencies, Multiexplorer might not run properly."
	exit 1
else
	@echo "All dependencies seems fine."
endif

#sniper:
#	make
#	wget wget http://snipersim.org/packages/sniper-benchmarks.tbz
#	tar xvf sniper-benchmarks.tbz
#	/multiexplorer/sniper-7.4/benchmarks
#	apt install -y gfortran
#	apt install -y m4
#	apt install -y xsltproc
#	apt install -y pkg-config
#	apt install -y gettext
#	apt install -y libx11-dev
#	apt install -y libxext-dev
#	apt install -y libxt-dev
#	apt install -y libxmu-dev
#	apt install -y libxi-dev