import csv
import json
import hashlib

import strconv
import pandas
import numpy
from flask import Flask, request, jsonify

import settings
from datastore import AmazonMediaStorage

from actions import actions
from dispatch import map_action

# Init App
app = Flask(__name__)
app.config.from_object(settings)

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    # Set up vars
    has_consistent_types = True
    sep = request.args.get('sep')

    if 'csv' in request.files:
        f = request.files['csv']
        data = pandas.read_csv(f, sep=sep) if sep else pandas.read_csv(f)
        result = data.to_json(orient='records')
        hasher = hashlib.sha1()
        hasher.update(result)
        _id = hasher.hexdigest()

        storage = AmazonMediaStorage(app, _id)
        storage.put(result, _id)

    return jsonify({
        '_meta': {
        },
        '_actions': {
            '_available': [key for key, value in actions.iteritems()],
            '_processed': []
        },
        '_record': {
            '_id': _id,
            '_current_revision': _id,
            '_all_revisions': storage.list_revisions()
        },
        'data': json.loads(result)
    }), 200


@app.route('/<_id>', methods=['GET'], defaults={'_revision': None})
@app.route('/<_id>/<_revision>')
def resource(_id, _revision):
    data = None
    r = None
    storage = AmazonMediaStorage(app, _id, create=False)
    available_actions = [key for key, value in actions.iteritems()]

    if storage:
        current = _revision if _revision else _id
        raw_data, current_meta = storage.get(current)
        data = pandas.read_json(raw_data)
        if not data.empty:
            request_actions = request.args.get('actions')
            if request_actions:
                a = json.loads(request_actions)
                for item in a:
                    fname = item.get('action', None)
                    columns = item.get('columns', None)
                    data, applied = map_action(fname, data, columns)
                    if applied:
                        if 'actions' in current_meta:
                            current_actions = json.loads(current_meta['actions'])
                            current_actions.append(item)
                            current_meta['actions'] = json.dumps(current_actions)
                        else:
                            current_meta['actions'] = json.dumps([item])

                result = data.to_json(orient='records')
                hasher = hashlib.sha1()
                hasher.update(result)
                revision = hasher.hexdigest()
                if revision is not current:
                    r = storage.put(result, revision, metadata=current_meta)

                return jsonify({
                    '_meta': {
                    },
                    '_actions': {
                        '_available': available_actions,
                        '_processed': json.loads(current_meta['actions'])
                    },
                    '_record': {
                        '_id': _id,
                        '_current_revision': revision if r else current,
                        '_all_revisions': storage.list_revisions()
                    },
                    'data': json.loads(result)
                })
            else:
                result = data.to_json(orient="records")
                return jsonify({
                    '_meta': {
                    },
                    '_actions': {
                        '_available': available_actions,
                        '_processed': json.loads(current_meta['actions']) \
                            if 'actions' in current_meta else []
                    },
                    '_record': {
                        '_id': _id,
                        '_current_revision': _revision if _revision else _id,
                        '_all_revisions': storage.list_revisions()
                    },
                    'data': json.loads(result)
                })
    return jsonify({
        'status': 404,
        'msg': 'Not found'
    }), 404
