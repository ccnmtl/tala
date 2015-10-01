# Django settings for tala project.
import os.path
from ccnmtlsettings.shared import common

project = 'tala'
base = os.path.dirname(__file__)

locals().update(
    common(
        project=project,
        base=base,
    ))

USE_TZ = True

INSTALLED_APPS += [  # noqa
    'bootstrapform',
    'tala.main',
]

PROJECT_APPS = ['tala.main', ]

WINDSOCK_BROKER_URL = "tcp://localhost:5555"
ZMQ_APPNAME = "tala"
WINDSOCK_SECRET = "6f1d916c-7761-4874-8d5b-8f8f93d20bf2"
WINDSOCK_WEBSOCKETS_BASE = "ws://localhost:5050/socket/"
