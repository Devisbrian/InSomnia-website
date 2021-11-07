import logging

from smtplib import SMTPException
from threading import Thread

from flask import current_app, url_for
from flask_mail import Message

from app import mail, urltimed

logger = logging.getLogger(__name__)


def _send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except SMTPException:
            logger.exception("Ocurrió un error al enviar el email")


def send_email(subject, sender, recipients, text_body,
               cc=None, bcc=None, html_body=None):
    msg = Message(subject, sender=sender, recipients=recipients, cc=cc, bcc=bcc)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    Thread(target=_send_async_email, args=(current_app._get_current_object(), msg)).start()

def mail_verification(email, username):
    # Crear token de verificación de correo
    token = urltimed.dumps(email, salt='email-confirm')
    link = url_for('auth.email_confirm', token=token, _external=True)
    # Enviamos un email de bienvenida
    send_email(subject='Welcome to the dreamworld',
                sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                recipients=[email, ],
                text_body=f'Hola {username}, ahora eres parte de InSomnia Colombia.',
                html_body=f'<p>Hola <strong>{username}</strong>, ahora eres parte de InSomnia Colombia</p><br>Confirma tu Email a través del siguiente link: {link} <br> *Este link expirará en 24 horas')
    