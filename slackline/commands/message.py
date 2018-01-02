from json import dumps
import sys

from slackline.slack.api import SlackClient
from .base import Base


class Message(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slack = SlackClient()

    def run(self):
        if self.options.get('-') is True:
            msg = sys.stdin.read()
            to = self.options.get('TO')
            sys.stdout.write('{}\n'.format(dumps({'msg': msg, 'to': to})))
            self.slack.send_message(to, msg)
