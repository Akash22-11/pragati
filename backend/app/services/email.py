import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

def send_email(to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = settings.MAIL_EMAIL
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(settings.MAIL_EMAIL, settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_EMAIL, to, msg.as_string())

def send_submission_confirmation(student_email, student_name, title):
    subject = 'Pragati - Submission Received'
    body = '<h2>Hi ' + student_name + '</h2><p>Your submission ' + title + ' is pending review.</p>'
    send_email(student_email, subject, body)

def send_admin_new_submission(student_name, title, category):
    subject = 'Pragati - New Submission'
    body = '<h2>New Submission</h2><p>Student: ' + student_name + '</p><p>Title: ' + title + '</p>'
    send_email(settings.ADMIN_EMAIL, subject, body)

def send_verification_result(student_email, student_name, title, action, note=None):
    subject = 'Pragati - Submission Update'
    body = '<h2>Hi ' + student_name + '</h2><p>Your submission ' + title + ' status: ' + str(action) + '</p>'
    send_email(student_email, subject, body)
