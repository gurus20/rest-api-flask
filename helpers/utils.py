from flask_mail import Message, Mail
from flask import current_app, render_template

mail = None

def send_mail(recipients, subject, template, **kwargs):
    global mail
    if not mail:
        mail = Mail(current_app)

    msg = Message(
        subject=subject, 
        sender ='notify@bracketcoders.com', 
        recipients = recipients 
    ) 
    msg.html = render_template(template, **kwargs)
    mail.send(msg)
