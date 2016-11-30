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

    def __init__(self, *args, **kwargs):
        self._db = None

    def connect(self, **kwargs):
        table_name = os.environ["LAZYSUSAN_SESSION_DYNAMODB_TABLE_NAME"]
        aws_region = os.environ["LAZYSUSAN_SESSION_AWS_REGION"]

        if not self._db:
            self._db = boto3.resource("dynamodb", region_name=aws_region)
            self._table = self._db.Table(table_name)

            data = self._table.get_item(Key=kwargs)
            record = data.get('Item', {})
            self.update(record)

    def save(self):
        item = {k: v for k, v in self.iteritems()}
        return self._table.put_item(Item=item)
