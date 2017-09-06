# CSV to JSON

REST API to profile, validate and transform CSV data to various structured data formats (especially JSON). The goal is to make cleaning and importing crappy data to various data stores less painful.

## API features

Examples below use [httpie](https://github.com/jakubroztocil/httpie). There's a usage cheatsheet at [http://ricostacruz.com/cheatsheets/httpie](http://ricostacruz.com/cheatsheets/httpie) if you're not familiar with the cli tool.

---

Upload a tsv file:

```
http -f POST localhost:5000 csv@file.csv sep=='\t'
```

Or a csv file:

```
http -f POST localhost:5000 csv@file.csv
```

This should give a response similar to what's shown below:

```
{
    "_actions": {
        "_available": [
            "convert_to_ascii_with_html",
            "remove_quotes",
            "split_by_comma",
            "infer_types",
            "convert_to_ascii_with_ignore"
        ],
        "_processed": []
    },
    "_meta": {},
    "_record": {
        "_all_revisions": [
            "a0a0c79d3b735499cfcacc82b8116cf6014322f7",
        ],
        "_current_revision": "a0a0c79d3b735499cfcacc82b8116cf6014322f7",
        "_id": "a0a0c79d3b735499cfcacc82b8116cf6014322f7"
    },
    "data": [
        {
            "column": "value",
        },
        ...
    ]
}
```

The response contains the data from the CSV or TSV converted to JSON, an id for the dataset, a number of `actions` available to run on the data, a list of ids for different revisions that have been created from the data, and the revision of the returned data.

---

You can now retrieve this dataset using it's `_id`, which will give you the same response as above:

```
http localhost:5000/a0a0c79d3b735499cfcacc82b8116cf6014322f7
```

Or you can retrieve a certain revision of this dataset using the revision's id. The first revision has the same id as the entire dataset:

```
http localhost:5000/a0a0c79d3b735499cfcacc82b8116cf6014322f7/a0a0c79d3b735499cfcacc82b8116cf6014322f7
```

---

You can perform actions listed in `available_actions` using a query string. Actions can be applied to every item in every column:

```
http localhost:5000/<id> actions=='[{"action":"convert_to_ascii_with_ignore"}]'
```

Or you can apply actions to every item in certain columns:

```
http localhost:5000/<id> actions=='[{"action":"convert_to_ascii_with_ignore", "columns":["column_one","column_two"]}]'
```

Using just an `_id` will apply the action to the first revision, while also passing a revision number will apply the action to a specific revision from the dataset:

```
http localhost:5000/<id>/<revision> actions=='[{"action":"convert_to_ascii_with_ignore", "columns":["column_one","column_two"]}]'
```

Response from running an action will add new revisions to the list of `_all_revisions`. Each revision shows which actions have been run to produce that version of the data. These are listed in `_processed`.
