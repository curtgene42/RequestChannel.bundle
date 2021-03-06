from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate
import smtplib
import traceback

DEFAULT_SERVER = ""
DEFAULT_PORT = 25

def validateEmail(email):
    if len(email) > 7:
        if re.match("^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,}$", email) is not None:
            return True
    return False

def setDefaultServer(server):
    global DEFAULT_SERVER
    DEFAULT_SERVER = server

def setDefaultPort(port):
    global DEFAULT_PORT
    DEFAULT_PORT = port


def send(email_from, email_to, subject, body, server=None, port=-1, username="", password="", secure=False, email_type="html", plain_body=None):
    if not server:
        server = DEFAULT_SERVER
    if port < 0:
        port = DEFAULT_PORT
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    if email_type == "html" and plain_body:
        msg.attach(MIMEText(plain_body, 'plain'))
    msg.attach(MIMEText(body, email_type))
    smtp = None
    try:
        smtp = smtplib.SMTP(server, port)
        if secure:
            smtp.starttls()
        if username:
            smtp.login(username, password)
        senders = smtp.sendmail(email_from, email_to, msg.as_string())
        smtp.quit()
        if not senders:
            return True
    except Exception as e:
        if smtp:
            smtp.quit()
        Log.Debug("Error in sendEMail: " + e.message)
        Log.Error(str(traceback.format_exc()))  # raise last error
    return False
