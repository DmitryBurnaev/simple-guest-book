import os
import random

from flask import Flask, jsonify, abort, request, make_response
from sqlalchemy.exc import DatabaseError

from database import db_session
from models import GuestRecord
from src.data import RECORDS

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/api/records/', methods=['GET'])
def get_records():
    records_query = GuestRecord.query.order_by('created_at').all()
    records = [record.to_dict() for record in records_query]
    return jsonify({'ok': True, 'records': records})


@app.route('/api/records/', methods=['POST'])
def add_record():
    record_data = request.get_json()
    try:
        author, message = record_data.get('author'), record_data.get('message')
        assert author and message, '`author` and `message` are required fields'
    except AssertionError as e:
        return make_response(jsonify({'ok': False, 'message': str(e)}), 400)

    record = GuestRecord(author, message)
    db_session.add(record)
    db_session.commit()
    return jsonify({'ok': True})


@app.route('/api/records/<int:record_id>/', methods=['DELETE'])
def delete_records(record_id):
    record = GuestRecord.query.filter_by(id=record_id).one()
    if not record:
        return make_response(
            jsonify({'ok': False, 'message': 'record not found'}),
            404
        )
    db_session.query(GuestRecord).filter_by(id=record_id).delete()
    # GuestRecord.query.filter_by(id=record_id).delete()
    # try:
    #     db_session.commit()
    # except DatabaseError as e:
    #     db_session.rollback()
    #     raise e
    return jsonify({'ok': True})


if __name__ == '__main__':
    app.run(host=os.environ.get('FLASK_APP_HOST', '127.0.0.1'),
            port=os.environ.get('FLASK_APP_PORT', '5000'),
            debug=os.environ.get('FLASK_DEBUG', False))
