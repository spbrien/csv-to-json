import os

import bucketstore
from flask import current_app

class AmazonMediaStorage():
    """
    Amazon S3 media storage
    """

    def __init__(self, app, _id, create=True):
        """
        Logs in to the database or storage service
        Creates a new table, set, bucket, whatever per CSV / dataset
        """
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
        Get an object from storage.
        Returns a tuple of the data and the metadata of the object
        """
        item = self.bucket.key(revision)
        meta = item.meta
        return self.bucket[revision], meta \
            if revision in self.bucket.list() else None

    def put(self, content, revision, metadata={}):
        """
        Put an object in storage, saves metadata with the object,
        returns the data from the object if successful,
        else returns None
        """
        if self.exists(revision):
            return self.get(revision)
        else:
            try:
                item = self.bucket.key(revision)
                item.set(content, metadata=metadata)
                return content
            except Exception as e:
                current_app.logger.error(e)
                return None

    def delete(self, revision):
        """
        Deletes the file referenced by revision.
        Returns nothing
        """
        if self.exists(revision):
            item = self.bucket.key(revision)
            item.delete()

    def exists(self, revision):
        """ Returns True if an object referenced by the given name or unique id
        already exists in the storage system, or False if the name is available
        for a new file.
        """
        return revision in self.bucket.list()
