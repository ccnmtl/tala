APP=tala
JS_FILES=media/js/irc.js
MAX_COMPLEXITY=4

all: jenkins

include *.mk

compose-migrate:
	docker-compose run web python manage.py migrate --settings=$(APP).settings_compose

compose-run:
	docker-compose up
