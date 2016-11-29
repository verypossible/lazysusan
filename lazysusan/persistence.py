import boto3
import os


class Memory(dict):

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def connect(self, **kwargs):
        pass

    def save(self):
        pass


class DynamoDB(dict):

    TABLE_NAME = os.environ["LAZYSUSAN_DYNAMODB_TABLE_NAME"]
    AWS_REGION = os.environ["LAZYSUSAN_AWS_REGION"]

    def __init__(self, *args, **kwargs):
        self._db = None

    def connect(self, **kwargs):
        if not self._db:
            self._db = boto3.resource("dynamodb", region_name=self.AWS_REGION)
            self._table = self._db.Table(self.TABLE_NAME)

            data = self._table.get_item(Key=kwargs)
            record = data.get('Item', {})
            self.update(record)

    def save(self):
        item = {k: v for k, v in self.iteritems()}
        return self._table.put_item(Item=item)
