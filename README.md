# CSV to JSON

Work in progress. The goal is a REST API to profile, validate and transform CSV data to various structured data formats (especially JSON). Ideally this would make cleaning and importing crappy data to various data stores less painful.

## Requirements

* [pip](https://pip.pypa.io/en/stable/installing/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

## Installation

```bash
# Make a new directory for your project
mkdir my-new-project
cd my-new-project

# Create a python virtual environment
virtualenv venv
source venv/bin/activate

# Install python dependencies
pip install -r requirements.txt

# Copy the settings.py.template file
cp settings.py.template settings.py

# **Be Sure to fill out AWS credentials in the newly created settings.py file**

# Run a local dev instance
./run.sh
```


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

The response contains the data from the CSV or TSV converted to JSON, an `_id` for the dataset, a number of `_actions` available to run on the data, a list of ids for different revisions that have been created from the data, and the revision of the returned data.

---

You can now retrieve this dataset using its `_id`, which will give you the same response as above:

```
http localhost:5000/<id>
```

Or you can retrieve a certain revision of this dataset using the revision's id. The first revision has the same id as the entire dataset:

```
http localhost:5000/<id>/<revision>
```

---

You can perform actions listed in `_available` using a query string. Actions can be applied to every item in every column:

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

## TODO

* Document deployment process
* Error checking, tests, and bugs
* Package project into stand-alone library with cli, init script, and scaffolding
* Add a plugins system so that new action functions can be created easily
