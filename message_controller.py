import os
from twilio.rest import Client


class MessageController:
    """ Twilio to send SMS """
    def __init__(self):
        self.sid = os.environ.get("TWILIO_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.phone_from = os.environ.get("TWILIO_PHONE_FROM")
        self.phone_to = os.environ.get("TWILIO_PHONE_TO")

    def send_sms(self, msg: str):
        """ send an SMS message """
        auth_token = self.auth_token
        account_sid = self.sid
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=msg,
            from_=self.phone_from,
            to=self.phone_to,
        )

        print(message.status)
