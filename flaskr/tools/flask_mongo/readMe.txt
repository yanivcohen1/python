https://github.com/paurakhsharma/flask-rest-api-blog-series

mkdir movie-bag
cd movie-bag

//First of all install pipenv using command
# linux
pip install --user pipenv
# windows
pip install pipenv

// create the virtual envirment
py -m venv venv

// ACTIVE IT
venv\Scripts\activate

// install Pipfile
//pipenv install flask
//pipenv install

// install
# windows
    pip install -e .
# linux
    $pip install --user pipenv
    $pip install --user -e .

//Now, let's install flask using pipenv
// THIS will create the Pipfile config
//pipenv install flask
//pipenv install

// for run the app
// in dev manualy
sh C:\Users\yaniv\OneDrive\python-flask\flaskr\tools\flask_mongo\dev.sh

//pipenv shell
# linux
export ENV_FILE_LOCATION=./.env.test
export ENV_FILE_LOCATION=./.env

# windows PS
$env:ENV_FILE_LOCATION = "./.env.test"
$env:ENV_FILE_LOCATION = "./.env"

# windows cmd
set ENV_FILE_LOCATION = "./.env.test"
set ENV_FILE_LOCATION = "./.env"

python app.py

//Add configuration for our MAIL_SERVER in .env

JWT_SECRET_KEY = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
+MAIL_SERVER: "localhost"
+MAIL_PORT = "1025"
+MAIL_USERNAME = "support@movie-bag.com"
+MAIL_PASSWORD = ""


//Start a SMTP server in next terminal with:

python -m smtpd -n -c DebuggingServer localhost:1025
//This will create an SMTP server for testing our email feature.

// on windows
.\run.bat

// on linux
sh .\run.sh

//Now run the app with
//python run.py
$env:FLASK_APP = ".\app.py"
$env:FLASK_ENV = "development"
flask run

// needed at least mongoDB ver 3.6
// get all movies for all users
http://127.0.0.1:5000/api/movies

// test It
python -m unittest tests/test_signup.py

// instal .env
pip install python-dotenv

// signup
http://127.0.0.1:5000/api/auth/signup
post body raw json:
{
    "email": "yaniv@gmail.com",
    "password": "123456"
}

// login and get token
http://127.0.0.1:5000/api/auth/login
post body raw json:
{
    "email": "yaniv@gmail.com",
    "password": "123456"
}

// add movie
http://127.0.0.1:5000/api/movies
post body raw json:
authorization bearer token: {from login with no ""}
{
    "name": "yaniv5@gmail.com",
    "casts": ["yaniv3"],
    "genres": ["cohen3"],
    "embeds": [{"name": "yan1", "value": "con1"}]
}

// test it: get query
http://127.0.0.1:5000/api/movies/637fa5b20563ba13bf6a3636
authorization bearer token: {from login with no ""}

// get query
http://127.0.0.1:5000/api/movie?name=yaniv5@gmail.com&name2=yan1&value=con1
result is : [{"_id": {"$oid": "637fa5b20563ba13bf6a3636"}, "name": "yaniv5@gmail.com", "casts":
["yaniv5"], "genres": ["cohen5"], "embeds": [{"name": "yan1", "value": "con1"}], "added_by":
{"$oid": "637f3f586f953a55081b5c96"}}]

// advanced-queries
// https://docs.mongoengine.org/guide/querying.html#advanced-queries

// Get published posts
Post.objects(Q(published=True) | Q(publish_date__lte=datetime.now()))

// Get top posts
Post.objects((Q(featured=True) & Q(hits__gte=1000)) | Q(hits__gte=5000))

//pip show packeg version
pip show flask
