"""Methods and mock classes for testing backup.py"""

from mongobackupd import backup, settings
import unittest

class MockConnection(object):
    """Mock of Boto EC2 connection"""
    def trim_snapshots(self, hourly_backups, daily_backups, monthly_backups):
        return [hourly_backups, daily_backups, monthly_backups]

class TestBackup(unittest.TestCase):
    """Tests for backup functions"""
    def test_mongo_url(self):
        """get_mongo_url should concat mongo credentials and host"""
        actual = backup.get_mongo_url("testHost")
        expected = "mongodb://" + \
        settings.MONGO_USERNAME + ":" + \
        settings.MONGO_PASSWORD + "@" + \
        "testHost" + settings.MONGO_PORT + "/" + \
        settings.MONGO_DATABASE
        self.assertEqual(actual, expected)
    def test_trim_snapshots(self):
        """calls boto trim_snapshots with gisettings"""
        connection = MockConnection()
        response = backup.trim_snapshots(connection)
        self.assertEqual(
            response,
            [settings.RETAIN_HOURLY, settings.RETAIN_DAILY, settings.RETAIN_MONTHLY]
            )
