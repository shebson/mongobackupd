"""Methods for printing logs and sending them to Slack"""

from slacker import Slacker
import settings

def get_slack():
    """Gets Slacker instance from settings"""
    if settings.SLACK_TOKEN:
        return Slacker(settings.SLACK_TOKEN)
    else:
        return None

def slack_message(slack, channel, message):
    """Send message to slack channel specified in settings.py"""
    if slack:
        return slack.chat.post_message(channel, message)
    return False

def log_message(message):
    """Prints message to stdout and slack if configured"""
    slack_message(get_slack(), settings.SLACK_CHANNEL, message)
    print (message)

def success(message):
    """Send success message"""
    log_message(message)
    return message

def error(message):
    """Send error message"""
    message = "ERROR: " + message
    log_message(message)
    return message
