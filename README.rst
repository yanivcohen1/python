# static type checking
Pylance: command palette: Preferences: Open User Settings (JSON) add "python.analysis.typeCheckingMode": "strict"

// for testting python ident run
python -tt
Flaskr
======

The basic blog app built in the Flask `tutorial`_.

.. _tutorial: http://flask.pocoo.org/docs/tutorial/

To add dependencys lib in file "setup.py"in setup(install_requires=["dependencyslibName"])

Remove from git path/to/folder/ or path/to/file.extention
===========
git clone --mirror https://github.com/yanivcohen1/python.git
cd python.git
pip install git-filter-repo
git filter-repo --path internal/git/path/to/folder/ --invert-paths
git remote add origin https://github.com/yanivcohen1/python.git
git push origin --force --all
git push --force
git push [origin] --force --all

Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the master branch. ::

    # clone the repository
    $ git clone https://github.com/pallets/flask
    $ cd flask
    # checkout the correct version
    $ git tag  # shows the tagged versions
    $ git checkout latest-tag-found-above
    $ cd examples/tutorial

update python and pip
    $ python -m pip install --upgrade pip

cheak pkg version istall:
    $ pip show pkg_name
    # or all
    $ pip list

Create a virtualenv and activate it::

    # linux
    # for linux create virtual envirment
    sudo apt install python3.8-venv
    $ python3 -m venv .venv
    $ . .venv/bin/activate

    # windows
    $ py -3.12 -m venv venv
    $ py -m venv venv
	  $ python -m venv venv
    $ venv\Scripts\activate
    # Create a virtual environment using the full path to the Python executable version X.Y
    $ /path/to/spcific_python_version/python.exe -m venv myenv
    $ venv\Scripts\activate
    $ venv\Scripts\activate.bat # for cmd not ps

    # create requirements.txt
    pip freeze > requirements.txt
    // install the requirements
    pip install -r requirements.txt

    # test it in cmd
    python -m pip -V
    where.exe python
    # or in PS
    python -v # control+Z to exit
    # in linux
    which python3

    on linux use pip3 and python3

# run jupyter notebook in env with the venv
jupyter nbconvert --to script file.ipynb
python file.py
//or
papermill file.ipynb output.ipynb

# linux remove the carriage return characters from win
sed -i 's/\r$//' your_script.sh

# kill script
sudo pkill -f runOllamaChatProxy.sh

Add to windows path:
C:\Users\yaniv\anaconda3
C:\Users\yaniv\anaconda3\Scripts;
C:\Users\yaniv\anaconda3\Library\bin
//install
pip install virtualenv
//for anaconda3 open powerShell in admin and type:
Set-ExecutionPolicy RemoteSigned
// then "control"+"shift"+"p" and type "reload window"

Or on Windows cmd::

    $ py -m venv venv
    $ venv\Scripts\activate.bat
    $ venv\Scripts\activate
    // to enable running script.ps1 in "Admin" mode run
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine

Install Flaskr::

    # windows
    # install pakeges in venv at editable mode (the source)
    pip install -e .
    # or install pakeges in venv at standart mode
    py -m pip install .

    # linux
    $pip install --user pipenv
    $pip install --user -e .

Or if you are using the master branch, install Flask from source before
installing Flaskr::

    $ pip install -e ../..
    $ pip install -e .
    $ pip install --upgrade -e .

// test it
python -c "import flask; print(flask.__version__)"

// to upgrade package_name
pip install package_name --upgrade

// stop it
control + c
#linux
control + z
Run
---


// To run the server
# on linux
sh ./run.sh
# on windows
./run.sh

//or manualy read params from the .env file
# linux
export ENV_FILE_LOCATION=./.env.test
export ENV_FILE_LOCATION=./.env

# windows PS
$env:ENV_FILE_LOCATION = "./.env.test"
$env:ENV_FILE_LOCATION = "./.env"

# windows cmd
set ENV_FILE_LOCATION = "./.env.test"
set ENV_FILE_LOCATION = "./.env"

//Now run the app with
//python run.py
$env:FLASK_APP = "./app.py"
$env:FLASK_ENV = "development"
flask run
// or in dev - debug mode
python run.py

// set the params manualy
on linux ::

    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run

on PS ::

    > $env:FLASK_APP = "flaskr"
    > $env:FLASK_ENV = "development"
    // > $env:FLASK_DEBUG = "true" // for flask 2.3
    > flask init-db
    > flask run

    to run the angular server.py > $env:FLASK_APP = ".\flaskr\server.py"
    flask run
    yarn
    yarn start
    Open http://127.0.0.1:4200 in a browser.

Or on Windows cmd::

    cd .\flaskr\
    > set FLASK_APP=flaskr
    > set FLASK_ENV=development
    > flask init-db
    > flask run

//run the .\flaskr\app.py
Open http://127.0.0.1:5000 in a browser.
username: yaniv
pass: 1234

Debug in vsc
------------
run in debug window task: 'Python: Flask'
or
python -m debugpy --listen 5678 ./fileName.py
and run "Python: Attach"

Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser

Deploy
------
https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/
https://github.com/pallets/flask/tree/master/examples/tutorial
python3 -m ensurepip --default-pip
python3 -m pip install --upgrade pip setuptools wheel
pip install wheel
//python setup.py sdist
python setup.py sdist bdist_wheel
this creacte a dist directory with two files theSourceCode.tar.gz & libs.whl

Run with a Production machine
-----------------------------
Create a virtualenv as above describe
pip install wheel
pip install flaskr-1.0.0-py3-none-any.whl
Run as above describe

Run as production server
------------------------
pip install waitress
pip install wheel
disable the firewall comodo
Create a virtualenv as above describe
Run as above describe without the development variable
waitress-serve --port=5000 --call 'flaskr:create_app'
// --call 'module:function'
// module is the file name.
// need to import the fileName from mainModule

To upload the dist to pip server
-------------------------
pip3 install twine
twine upload dist/*
// to download and install it from pip
pip install <projectName>

To upgrade latest
--------------------------
pip install <package_name> --upgrade

To complie proj to pyc:
--------------------------
python -m compileall .
// and run it:
python yourfile.pyc
