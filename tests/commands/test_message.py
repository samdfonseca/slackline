import sys
from io import StringIO
from subprocess import PIPE, Popen as popen
from unittest import mock

from slackline.commands import Message

import pytest


@pytest.fixture
def message():
    options = {'-': True,
            '--help': False,
            '--version': False,
            'TO': '@sam',
            'message': True,
            }
    message = Message(options)
    message.slack.send_message = mock.MagicMock()
    return message


@pytest.fixture(autouse=True)
def mock_stdin():
    stdin_orig = sys.stdin
    sys.stdin = StringIO()
    yield
    sys.stdin = stdin_orig


def write_stdin(val: str):
    sys.stdin.write(val)
    sys.stdin.seek(0)


def test_calls_send_message(message):
    write_stdin('sam test')
    message.run()
    message.slack.send_message.assert_called_with('@sam', 'sam test')


def test_call_send_message_multiline(message):
    write_stdin('sam\ntest')
    message.run()
    message.slack.send_message.assert_called_with('@sam', 'sam\ntest')

