'''
install requirements:
pip install requests
pip install pyquery
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
from constants import JOB_REGEX

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
    job_list = jQuery('.job-list').text()
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
