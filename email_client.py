import smtplib
import logging
import os
import inspect

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(os.path.splitext(os.path.basename(inspect.getfile(inspect.currentframe())))[0])


def send_email(email_object, message):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email_object['address'], email_object['password'])
        logger.debug('Sending message: ' + str(message))
        server.send_message(message)
        server.close()
        logger.info('email succesfully sent')
    except Exception as error:
        logger.error('Problem occured in send_email: ' + str(error), exc_info=True)
