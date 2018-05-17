from flask import Flask, json, jsonify, abort, request

from src.data import RECORDS

app = Flask(__name__)


@app.route('/api/records/', methods=['GET'])
def get_records():
    return jsonify({'ok': True, 'records': RECORDS})


@app.route('/api/records/', methods=['POST'])
def add_record():
    RECORDS.append({
        'id': request.form['id'],
        'author': request.form['author'],
        'message': request.form['message'],
    })
    return jsonify({'ok': True})


@app.route('/api/records/<int:record_id>/', methods=['DELETE'])
def delete_records(record_id):
    for index, item in enumerate(RECORDS):
        if item['id'] == record_id:
            RECORDS.pop(index)
            break
    else:
        abort(404, 'Record does not found')
    return jsonify({'ok': True})


