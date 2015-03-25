"""Settings for the mongo backup daemon"""

# AWS Credentials
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR_AWS_SECRET_KEY"

# MongoDB Credentials
MONGO_USERNAME = "YOUR_MONGO_USERNAME"
MONGO_PASSWORD = "YOUR_MONGO_PASSWORD"
MONGO_DATABASE = "YOUR_MONGO_DB"
MONGO_PORT = ":27017"

# EC2 Instace Filter
# The example below targets enstances whose name starts with "mongo-"
INSTANCE_FILTERS = {
    "tag:Name": "mongo-*"
}

# Sapshot retention settings
# The example below hourly snapshots for a day, daily snapshopts for a week,
# and monthly backups for a quarter
RETAIN_HOURLY = 24
RETAIN_DAILY = 7
RETAIN_MONTHLY = 3

# Slack settings
# To enable Slack integration, set SLACK_TOKEN to a non-None value
# To integrate with non-Slack chat or logging apps, edit reporting.py
SLACK_TOKEN = None
SLACK_CHANNEL = "#general"

# You backup schedules is set seperately in ./crontab
# For information on crontab syntax, see http://en.wikipedia.org/wiki/Cron
