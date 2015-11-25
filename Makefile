MANAGE=./manage.py
APP=tala
FLAKE8=./ve/bin/flake8

jenkins: ./ve/bin/python validate flake8 jshint jscs test

./ve/bin/python: requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

test: ./ve/bin/python
	$(MANAGE) jenkins --pep8-exclude=migrations --enable-coverage --coverage-rcfile=.coveragerc

flake8: ./ve/bin/python
	$(FLAKE8) $(APP) --max-complexity=8

runserver: ./ve/bin/python validate
	$(MANAGE) runserver

migrate: ./ve/bin/python validate jenkins
	$(MANAGE) migrate

validate: ./ve/bin/python
	$(MANAGE) validate

shell: ./ve/bin/python
	$(MANAGE) shell_plus

jshint: node_modules/jshint/bin/jshint
	./node_modules/jshint/bin/jshint --config=.jshintrc media/js/irc.js

jscs: node_modules/jscs/bin/jscs
	./node_modules/jscs/bin/jscs media/js/irc.js

node_modules/jshint/bin/jshint:
	npm install jshint --prefix .

node_modules/jscs/bin/jscs:
	npm install jscs --prefix .

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm celerybeat-schedule
	rm .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make validate
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make validate
	make test
	make migrate
	make flake8

build:
	docker build -t ccnmtl/tala .

compose-migrate:
	docker-compose run web python manage.py migrate --settings=tala.settings_compose

compose-run:
	docker-compose up


# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: ./ve/bin/python validate jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate
