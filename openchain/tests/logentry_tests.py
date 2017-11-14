from unittest import TestCase

from openchain.models.factory import ModelFactory
from openchain.models.logentry import LogEntry


class LogEntryModelTestCase(TestCase):

    def setUp(self):
        LogEntry.objects.delete_all()

    def test_logentry_creation(self):
        logentry = LogEntry('test message')
        logentry.save()

        self.assertIsInstance(logentry, LogEntry)
        LogEntry.objects.delete_all()

    def test_logentry_set(self):
        logentry = LogEntry('test message 01')
        logentry.save()
        logentry = LogEntry('test message 02')
        logentry.save()
        logentry_count = len(LogEntry.objects.get())

        self.assertEqual(logentry_count, 2)
        LogEntry.objects.delete_all()

    def test_logentry_model_factory(self):
        logentry_model_instance = ModelFactory.get_model('logentry')
        self.assertEqual(logentry_model_instance, LogEntry)
