import os
import unittest
from datetime import datetime

from flask import json

os.environ['TEST_ENV'] = '1'

from src import app
from src.models import GuestRecord
from src.database import create_db


class RestAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_db()
        cls.client = app.app.test_client()
        cls.db_session = app.db_session

    @classmethod
    def tearDownClass(cls):
        del os.environ['TEST_ENV']

    def status_ok(self, response, expected_status=200):
        self.assertEqual(response.status_code, expected_status)
        self.assertTrue(response.json['ok'])

    def test_list_records(self):
        record = GuestRecord(author_name='Test Name', message='Test message')
        self.db_session.add(record)
        self.db_session.commit()
        count_stored_records = self.db_session.query(GuestRecord).count()
        response = self.client.get('/api/records/')
        self.status_ok(response)
        self.assertIn(record.to_dict(), response.json['records'])
        self.assertEqual(len(response.json['records']), count_stored_records)

    def test_create_record(self):
        record = GuestRecord(author_name='Test Name', message='Test message')
        record.created_at = datetime.now()
        data = record.to_dict()
        del data['id']
        response = self.client.post('/api/records/',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.status_ok(response)
        response = self.client.get('/api/records/')
        response_record = [r for r in response.json['records']
                           if r['author_name'] == record.author_name][0]
        del response_record['id']
        self.assertDictEqual(response_record, data)

    def test_remove_record(self):
        record = GuestRecord(author_name='Test Remove', message='Test message')
        self.db_session.add(record)
        self.db_session.commit()
        response = self.client.delete('/api/records/{}/'.format(record.id))
        self.status_ok(response)

        response = self.client.get('/api/records/')
        self.status_ok(response)
        self.assertNotIn(record.to_dict(), response.json['records'])
        r = self.db_session.query(GuestRecord).filter_by(id=record.id).first()
        self.assertIsNone(r)



