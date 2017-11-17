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

    def test_logentry_get(self):
        queryset = LogEntry.objects.get()
        self.assertEqual(len(queryset), 0)

        LogEntry.objects.delete_all()

    def test_logentry_set(self):
        logentry_01 = LogEntry('test message 01')
        logentry_01.save()
        logentry_02 = LogEntry('test message 02')
        logentry_02.save()

        queryset = LogEntry.objects.get()
        self.assertEqual(len(queryset), 2)

        LogEntry.objects.delete_all()

    def test_logentry_search(self):
        logentry_01 = LogEntry('test message 01')
        logentry_01.save()
        logentry_02 = LogEntry('test message 02')
        logentry_02.save()

        queryset = LogEntry.objects.get()
        found_entry = LogEntry.objects.search(queryset[0])
        self.assertEqual(found_entry, logentry_01)

        LogEntry.objects.delete_all()
    def test_logentry_model_factory(self):
        logentry_model_instance = ModelFactory.get_model('logentry')

        self.assertEqual(logentry_model_instance, LogEntry)
