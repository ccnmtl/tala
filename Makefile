APP=tala
JS_FILES=media/js/irc.js

all: jenkins

include *.mk

compose-migrate:
	docker-compose run web python manage.py migrate --settings=$(APP).settings_compose

compose-run:
	docker-compose up
