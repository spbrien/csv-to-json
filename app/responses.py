import hashlib
import json

import pandas

from dispatch import map_action, map_analysis


def simple_result(actions, data, meta, storage, _revision, _id):
    result = data.to_json(orient="records")
    return {
        '_actions': {
            '_available': actions,
            '_processed': meta['actions'] \
                if 'actions' in meta else []
        },
        '_record': {
            '_id': _id,
            '_current_revision': _revision if _revision else _id,
            '_all_revisions': storage.list_revisions()
        },
        'data': json.loads(result)
    }

def process_actions(
        available_actions,
        actions,
        data,
        meta,
        storage,
        current,
        _revision,
        _id
    ):
    a = json.loads(actions)
    for item in a:
        fname = item.get('action', None)
        columns = item.get('columns', None)
        data, applied = map_action(fname, data, columns)
        if applied:
            if 'actions' in meta:
                current_actions = meta['actions']
                current_actions.append(item)
                meta['actions'] = current_actions
            else:
                meta['actions'] = [item]

    result = data.to_json(orient='records')
    hasher = hashlib.sha1()
    hasher.update(result)
    revision = hasher.hexdigest()
    if revision is not current:
        revised_data = storage.put(result, revision, metadata=meta)
    else:
        revised_data = None

    return {
        '_actions': {
            '_available': available_actions,
            '_processed': meta['actions']
        },
        '_record': {
            '_id': _id,
            '_current_revision': revision if revised_data else current,
            '_all_revisions': storage.list_revisions()
        },
        'data': json.loads(result)
    }


def process_analysis(available_analysis, analysis, data):
    data_dict = data.get('data', None)
    df = pandas.DataFrame.from_dict(data_dict)

    a = json.loads(analysis)
    data['_analysis'] = {
        '_available': available_analysis,
        '_processed': {}
    }
    for item in a:
        fname = item.get('action', None)
        column = item.get('column', None)
        if fname and column:
            key, value = map_analysis(fname, df, column)
            data['_analysis']['_processed'][key] = value

    return data
