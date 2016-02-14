#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib, configparser
from datetime import datetime


config = configparser.ConfigParser()
config.read('config.ini')


class EmailMeWhenReady:
    '''
    A decorator that sends an email when the decorated function has
    completed.
    '''
    def __init__(self, recipient=None):
        self.recipient = recipient
        if not self.recipient:
            self.recipient = config['gmail']['recipient']

    def __call__(self, func):
        self.func = func
        def wrapper(*args, **kwargs):
            self.start_time = datetime.now()
            self.result = self.func(*args, **kwargs)
            self.end_time = datetime.now()
            self.send_email()
            return self.result
        return wrapper

    def valid_recipient(self):
        '''
        Check if the given email address or addresses is/are valid.
        '''
        # TODO
        return True

    def send_email(self):
        '''
        Prepares and sends email.
        '''
        if not self.valid_recipient():
            Exception('Recipient ({0}) is not valid'.format(
                self.recipient))
        gmail_user = config['gmail']['user']
        gmail_pwd = config['gmail']['pwd']
        FROM = config['gmail']['user']
        TO = recipient if type(
            self.recipient) is list else [self.recipient]
        SUBJECT, TEXT = self.prepare_email_text()

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


    def prepare_email_text(self):
        '''
        Prepares the subect and body texts with details about the function
        name and the length of time it took for the function to run.
        '''
        self.time_taken = self.end_time - self.start_time
        SUBJECT = '{0} has finished'.format(self.func.__name__)
        TEXT = '{0} has finished and took {1}.\nStart: {2} \nEnd: {3}'.format(
            self.func.__name__, self.time_taken, self.start_time,
            self.end_time)
        return (SUBJECT, TEXT)
