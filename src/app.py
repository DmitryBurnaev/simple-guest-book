import argparse
import os

from flask import Flask, jsonify, request, make_response

from src.database import db_session, init_db
from src.models import GuestRecord

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/api/records/', methods=['GET'])
def get_records():
    records_query = GuestRecord.query\
        .order_by(GuestRecord.created_at.desc())\
        .all()
    records = [record.to_dict() for record in records_query]
    return jsonify({'ok': True, 'records': records})


@app.route('/api/records/', methods=['POST'])
def add_record():
    record_data = request.get_json()
    try:
        author = record_data.get('author_name')
        message = record_data.get('message')
        assert author and message, '`author` and `message` are required fields'
    except AssertionError as e:
        return make_response(jsonify({'ok': False, 'message': str(e)}), 400)
    print(author, message)
    record = GuestRecord(author, message)
    db_session.add(record)
    db_session.commit()
    return jsonify({'ok': True})


@app.route('/api/records/<int:record_id>/', methods=['DELETE'])
def delete_records(record_id):
    record = GuestRecord.query.filter_by(id=record_id).first()
    if not record:
        return make_response(
            jsonify({'ok': False, 'message': 'record was not found'}),
            404
        )
    db_session.query(GuestRecord).filter_by(id=record_id).delete()
    db_session.commit()
    return jsonify({'ok': True})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--createdb', action='store_true', default=False)
    args = parser.parse_args()
    if args.createdb:
        init_db()

    app.run(host=os.environ.get('FLASK_APP_HOST', '127.0.0.1'),
            port=os.environ.get('FLASK_APP_PORT', '5000'),
            debug=os.environ.get('FLASK_DEBUG', False))
