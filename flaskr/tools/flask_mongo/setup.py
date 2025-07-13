import io

from setuptools import find_packages
from setuptools import setup

with io.open("readMe.txt", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="flaskr",
    # python_requires='== 3.10.0',
    version="1.0.0",
    url="http://flask.pocoo.org/docs/tutorial/",
    license="BSD",
    maintainer="Pallets team",
    maintainer_email="contact@palletsprojects.com",
    description="The basic blog app built in the Flask tutorial.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    # add libs here
    # to add lib A version 1 and lib B at lest version 2 "'A>=1,<2', 'B>=2', c==3.1"
    install_requires=[
        "flask==2.2.2",
        "flask-mongoengine==1.0.0",
        "flask-restful==0.3.9",
        "flask-bcrypt==1.0.1",
        "flask-jwt-extended==4.3.1",
        "flask-mail==0.9.1",
        "flask_cors==3.0.10",
        "pylint",
        "pylint-flask",
        "pylint-flask-sqlalchemy"
        "mypy"
    ],
    extras_require={"test": ["pytest", "coverage"]},
)
