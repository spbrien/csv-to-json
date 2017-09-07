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
from responses import process_actions, simple_result

# Init App
app = Flask(__name__)
app.config.from_object(settings)

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    # Set up vars
    sep = request.args.get('sep')

    if 'csv' in request.files:
        f = request.files['csv']
        data = pandas.read_csv(f, sep=sep) if sep else pandas.read_csv(f)
        result = data.to_json(orient='records')
        hasher = hashlib.sha1()
        hasher.update(result)
        _id = hasher.hexdigest()

        storage = AmazonS3Storage(app, _id)
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
    storage = AmazonS3Storage(app, _id, create=False)
    available_actions = [key for key, value in actions.iteritems()]

    if storage:
        current = _revision if _revision else _id
        raw_data, current_meta = storage.get(current)
        data = pandas.read_json(raw_data)
        if not data.empty:
            # Get all transformation and analysis queries
            request_actions = request.args.get('actions')

            # Create an initial result
            result = None

            # Apply filters
            # TODO: Filtering

            # Apply actions
            if request_actions:
                result = process_actions(
                    available_actions,
                    request_actions,
                    data,
                    current_meta,
                    storage,
                    current,
                    _revision,
                    _id
                )

            # Apply validation / normalization
            # TODO: validation and normalization

            # If we didn't have actions or validation to apply
            if not result:
                result = simple_result(
                    request_actions,
                    data,
                    current_meta,
                    storage,
                    _revision,
                    _id
                )

            # Process Analysis and add _meta to result
            # TODO: write analysis functions

            return jsonify(result), 200

    return jsonify({
        'status': 404,
        'msg': 'Not found'
    }), 404
