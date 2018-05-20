import os
from flask import Flask, jsonify, request, make_response

from database import db_session
from models import GuestRecord, validate_record_data

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
    valid, message = validate_record_data(record_data)
    if not valid:
        return make_response(jsonify({'ok': False, 'message': message}), 400)

    record = GuestRecord(record_data['author_name'], record_data['message'])
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
    app.run(host=os.environ.get('FLASK_APP_HOST', '127.0.0.1'),
            port=os.environ.get('FLASK_APP_PORT', '5000'),
            debug=os.environ.get('FLASK_DEBUG', False))
