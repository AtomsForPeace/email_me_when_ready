from functools import wraps
import smtplib, configparser
from datetime import datetime


config = configparser.ConfigParser()
config.read('config.ini')


def email_me_when_ready(recipient=None):
    '''
    A decorator that sends an email when the decorated function has
    completed.
    '''
    if not recipient:
        recipient = config['gmail']['recipient']
    wraps(email_me_when_ready)
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            send_email(
                recipient=recipient, function_name=func.__name__,
                start_time=start_time, end_time=end_time)
            return result
        return wrapper
    return decorator


def valid_recipient(recipient):
    '''
    Check if the given email address or addresses is/are valid.
    '''
    # TODO
    return True


def send_email(recipient, function_name, start_time, end_time):
    '''
    Prepares and sends email.
    '''
    if not valid_recipient(recipient):
        Exception('Recipient ({0}) is not valid'.format(recipient))
    gmail_user = config['gmail']['user']
    gmail_pwd = config['gmail']['pwd']
    FROM = config['gmail']['user']
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT, TEXT = prepare_email_text(
        function_name, start_time, end_time)

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


def prepare_email_text(function_name, start_time, end_time):
    '''
    Prepares the subect and body texts with details about the function
    name and the length of time it took for the function to run.
    '''
    time_taken = end_time - start_time
    SUBJECT = '{0} has finished'.format(function_name)
    TEXT = '{0} has finished and took {1}.\nStart: {2} \nEnd: {3}'.format(
        function_name, time_taken, start_time, end_time)
    return (SUBJECT, TEXT)
