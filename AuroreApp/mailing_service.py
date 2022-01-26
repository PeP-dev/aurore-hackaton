from typing import List

import requests as requests


class Mail:
    def __init__(self, to: List[str], subject: str, text: str):
        self.to = to
        self.subject = subject
        self.text = text


class AbstractMailingService:
    def send_mail(self):
        raise Exception("not implemented")


class MailgunMailingService(AbstractMailingService):
    def __init__(self, api_key, domain):
        self.api_key = api_key
        self.domain = domain

    def send_mail(self, mail: Mail):
        return requests.post(
            "https://api.mailgun.net/v3/{domain}/messages".format(domain=self.domain),
            auth=("api", self.api_key),
            data={"from": "Mail automatique Entr'ACT <mailgun@{domain}>".format(domain=self.domain),
                  "to": mail.to,
                  "subject": mail.subject,
                  "text": mail.text})
