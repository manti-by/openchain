from unittest import TestCase

from openchain.models.logentry import LogEntry


class LogEntryTestCase(TestCase):

    def test_logentry_creation(self):
        logentry = LogEntry('test message')
        logentry.save()
        self.assertIsInstance(logentry, LogEntry)
