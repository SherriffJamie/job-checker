#!/usr/bin/env python
__author__ = "Jamie Sherriff"
__license__ = "MIT License"
__version__ = "1.0.0"
__maintainer__ = "Jamie Sherriff"
__contact__ = "https://github.com/jamie-sherriff"
__status__ = "Production"
__date__ = "12-03-2017"
'''
Simple script to check various webpages if jobs are available, reads in the url to scan from sys.argv
see requirements.txt for pip dependencies
'''
import requests
from pyquery import PyQuery
import traceback
import logging
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlparse
from email_client import send_email
from constants import JOB_REGEX, JOB_CSS_SEARCH_LIST

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])

SERVER_URL = None

try:
    SERVER_URL = sys.argv[1]
except IndexError as error:
    print('need to supply a URL as the first argument')
    logger.error('need to supply a URL as the first argument: ' + str(error), exc_info=True)
    sys.exit(1)

parse_result = urlparse(SERVER_URL)
if not bool(parse_result.scheme) and not bool(parse_result.netloc):
    logger.error(str(SERVER_URL) + " :server url needs to be valid", exc_info=True)
    raise ValueError(str(SERVER_URL) + " :server url needs to be valid")

SERVER_HOST = urlparse(SERVER_URL).netloc
email = {
    'address': os.environ.get('GMAIL_ADDRESS'),
    'password': os.environ.get('GMAIL_PASSWORD'),
    'reciever': os.environ.get('EMAIL_RECIPIENTS').split(',')
}
email_message = MIMEMultipart()
email_message['From'] = email['address']
email_message['To'] = ', '.join(email['reciever'])

try:
    response = requests.get(SERVER_URL, timeout=30)
    response.raise_for_status()
    raw_html = response.text
    jQuery = PyQuery(raw_html)
    job_list = None
    for job_css in JOB_CSS_SEARCH_LIST:
        job_list = jQuery(job_css).text()
        if job_list:
            break
    if not job_list:
        logger.info('Running job checker against: ' + SERVER_HOST + 'and could not parse page')
        email_message['Subject'] = "Job Checker could not parse page at: " + SERVER_HOST
        body = "Raw HTML FROM: " + SERVER_HOST + ":\n" + jQuery.html(method='html')
        email_message.attach(MIMEText(body, 'plain'))
        send_email(email, email_message)
    else:
        match = JOB_REGEX.search(job_list)
        email_message['Subject'] = "Jobs Available at: " + SERVER_HOST
        body = "Content Retrieved from " + SERVER_HOST + ":\n" + job_list
        email_message.attach(MIMEText(body, 'plain'))
        logger.debug('Found job_list: ' + job_list)
        if not match:
            logger.info('Jobs have appeared so sending email.')
            send_email(email, email_message)
        else:
            logger.info('Found no jobs so not sending email')
except Exception as error:
    logger.error('Found error in email process:', exc_info=True)
    email_message['Subject'] = SERVER_HOST + " Job Emailer Fault"
    exc_type, exc_value, exc_traceback = sys.exc_info()
    body = "Email fault recieved:\n" + repr(traceback.format_exception(exc_type, exc_value,
                                                                       exc_traceback))
    email_message.attach(MIMEText(body, 'plain'))
    send_email(email, email_message)
