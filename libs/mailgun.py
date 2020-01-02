# -*- coding: utf-8 -*-

"""Library for interacting with the Mailgun service."""

import os

from requests import post, Response
from typing import List


class MailgunException(Exception):
    """Mailgun exception handler."""
    message: str


class Mailgun(object):
    """Class for interacting with MailGun service.

    Attributes:
        FROM_NAME: The sender's name.
        FROM_EMAIL: The sender's email address.
    """

    FROM_NAME = 'Pricing Service'
    FROM_EMAIL = 'do-not-reply@sandboxf4a23711dba74ab69c683dd67a53db67.mailgun.org'

    @classmethod
    def send_mail(cls, recipients: List[str], subject: str,
                  body_text: str, body_html: str) -> Response:
        """Sends an email.

        Args:
            recipients: A list of email addresses to send to.
            subject: The email subject.
            body_text: The plaintext email body.
            body_html: The HTML email body.

        Returns:
            The HTTP response from Mailgun.

        Raises:
            MailgunException: If no api_key or domain has been set, or if the
                HTTP response is anything other than '200 OK'

        """
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        if api_key is None:
            raise MailgunException('Failed to load Mailgun API key.')

        domain = os.environ.get('MAILGUN_DOMAIN', None)
        if domain is None:
            raise MailgunException('Failed to load Mailgun API key.')

        response = post(f'{cls.MAILGUN_DOMAIN}/messages',
                        auth=('api', cls.MAILGUN_API_KEY),
                        data={'from': f'{cls.FROM_NAME} <{cls.FROM_EMAIL}>',
                              'to': recipients,
                              'subject': subject,
                              'text': body_text,
                              'html': body_html})

        if response.status_code != 200:
            raise MailgunException('An error occurred while sending email.')

        return response
