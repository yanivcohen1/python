git push -u origin main

# instractions
https://medium.com/@balramchavan/angular-python-flask-full-stack-demo-27192b8de1a3

# NgPythonDemo
This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 1.6.0.

## pre run python install
https://packaging.python.org/tutorials/managing-dependencies/
first disable comodo firewall 
python -m ensurepip --default-pip
python -m pip install --upgrade pip setuptools wheel
pip install --user pipenv
pipenv install requests
pipenv run python main.py
pipenv install Flask
pipenv install flask flask-jsonpify flask-sqlalchemy flask-restful
pipenv install flask-cors
pipenv run python server.py
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

## Development server
Run python server using `python server.py` command
pipenv run python server.py

# for run in dist
https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/
https://github.com/pallets/flask/tree/master/examples/tutorial
python setup.py sdist
python setup.py sdist bdist_wheel

## Development server
yarn
yarn start
Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `-prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
