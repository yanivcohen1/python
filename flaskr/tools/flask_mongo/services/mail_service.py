from threading import Thread
from flask_mail import Message
from flaskr.tools.flask_mongo.resources.errors import InternalServerError
# from flaskr.tools.flask_mongo.app import mail, app

def send_async_email(app, msg):
    from flaskr.tools.flask_mongo.app import mail
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise InternalServerError("[MAIL SERVER] not working")


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    from flaskr.tools.flask_mongo.app import app
    Thread(target=send_async_email, args=(app, msg)).start()
