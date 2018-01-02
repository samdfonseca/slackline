"""Tests for our main skele CLI module."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

from slackline import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['slackline', '-h'], stdout=PIPE).communicate()[0].decode()
        self.assertTrue('Usage:' in output)

        output = popen(['slackline', '--help'], stdout=PIPE).communicate()[0].decode()
        self.assertTrue('Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['slackline', '--version'], stdout=PIPE).communicate()[0].decode()
        self.assertEqual(output.strip(), VERSION)
