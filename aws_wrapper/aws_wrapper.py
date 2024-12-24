from aws_wrapper.storage import Storage
from aws_wrapper.database import Database
from aws_wrapper.queue import Queue
from aws_wrapper.compute import Compute


class AWSWrapper(Storage, Database, Queue, Compute):
    def __init__(self, region="us-east-1"):
        Storage.__init__(self, region)
        Database.__init__(self, region)
        Queue.__init__(self, region)
        Compute.__init__(self, region)
