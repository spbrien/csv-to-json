import os

import bucketstore
from flask import current_app

class AmazonMediaStorage():
    """
    Amazon S3 media storage
    """

    def __init__(self, app, _id, create=True):
        # Get settings from App config
        aws_access_key_id = app.config['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = app.config['AWS_SECRET_ACCESS_KEY']

        # Initialize our S3 Bucket
        bucketstore.login(aws_access_key_id, aws_secret_access_key)
        try:
            self.bucket = bucketstore.get(_id, create=create)
        except Exception as e:
            current_app.logger.error(e)
            return None

    def list_revisions(self):
        return self.bucket.list()

    def get(self, revision):
        """
        Get a file from storage
        """
        item = self.bucket.key(revision)
        meta = item.meta
        return self.bucket[revision], meta \
            if revision in self.bucket.list() else None

    def put(self, content, revision, metadata={}):
        """
        Put a file in storage
        """
        if self.exists(revision):
            return self.get(revision)
        else:
            try:
                item = self.bucket.key(revision)
                item.set(content, metadata=metadata)
                return self.get(revision)
            except Exception as e:
                current_app.logger.error(e)
                return None

    def delete(self, revision):
        """
        Deletes the file referenced by revision.
        """
        if self.exists(revision):
            item = self.bucket.key(revision)
            item.delete()

    def exists(self, revision):
        """ Returns True if a file referenced by the given name or unique id
        already exists in the storage system, or False if the name is available
        for a new file.
        """
        return revision in self.bucket.list()
