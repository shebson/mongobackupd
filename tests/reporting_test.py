"""Tests and mock classes for reporting.py"""

from mongobackupd import reporting
import unittest

class MockSlackerChat(object):
    """Mock of Slacker.chat exposes post_message"""
    def post_message(self, channel, message):
        """Concats and returns channel and message"""
        return channel + message

class MockSlacker(object):
    """Mock Slacker class"""
    def __init__(self):
        self.chat = MockSlackerChat()

class TestSlackIntegration(unittest.TestCase):
    """Tests for slack integration"""
    def test_slack_message_valid(self):
        """slack_message should send message when slack is not None"""
        slack = MockSlacker()
        channel = "foo"
        message = "bar"
        test_message = reporting.slack_message(slack, channel, message)
        self.assertEqual(
            test_message,
            channel + message,
            "slack_message did not send message when provided with Slacker instance"
            )
    def test_slack_message_no_slack(self):
        """slack_message should return false if no slack config"""
        slack = None
        channel = "foo"
        message = "bar"
        test_message = reporting.slack_message(slack, channel, message)
        self.assertEqual(
            test_message,
            False,
            "slack_message did not return False when provided with no Slacker instance"
            )

class TestMessageHandling(unittest.TestCase):
    """Tests for functions that handle messages"""
    def test_error_message(self):
        """reporting.error should prepend 'ERROR: ' to message"""
        returned = reporting.error("Ouch!")
        self.assertEqual(
            returned,
            "ERROR: Ouch!",
            "reporting.error did not correctly prepend 'ERROR: '")
    def test_success_message(self):
        """reporting.sucess should not modify message"""
        returned = reporting.success("Yay!")
        self.assertEqual(
            returned,
            "Yay!",
            "reporting.success changed message")

