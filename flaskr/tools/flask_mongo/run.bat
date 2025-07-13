REM set FLASK_ENV=production
REM set ENV_FILE_LOCATION=./.env.test

set FLASK_APP=./app.py
set FLASK_DEBUG=1
set FLASK_RUN_PORT=8001
set ENV_FILE_LOCATION=./.env.test
set FLASK_ENV=development

flask run