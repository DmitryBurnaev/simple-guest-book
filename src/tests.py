import os
import unittest
from datetime import datetime

from flask import json

PATH_TEST_DATABASE = os.environ.get('PATH_TEST_DATABASE', '/tmp/test.db')
os.environ['FLASK_DB_PATH'] = 'sqlite:///{}'.format(PATH_TEST_DATABASE)

from src import app
from src.models import GuestRecord


class RestAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(PATH_TEST_DATABASE):
            os.remove(PATH_TEST_DATABASE)
        app.init_db()
        cls.client = app.app.test_client()
        cls.db_session = app.db_session

    @classmethod
    def tearDownClass(cls):
        os.remove(PATH_TEST_DATABASE)
        if 'FLASK_DB_PATH' in os.environ:
            del os.environ['FLASK_DB_PATH']

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



