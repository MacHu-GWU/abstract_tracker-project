# -*- coding: utf-8 -*-

import time
import random
import dataclasses

import boto3
import moto

from abstract_tracker.logger import logger
from abstract_tracker.base import StatusEnum
from abstract_tracker.trackers.s3_tracker import T_ID, S3Tracker

mock_s3 = moto.mock_s3()
mock_s3.start()
bucket = "my-bucket"

s3_client = boto3.client("s3")
s3_client.create_bucket(Bucket=bucket)


@dataclasses.dataclass
class MyTracker(S3Tracker):
    @classmethod
    def get_bucket_key(self, id: T_ID):
        return bucket, f"{id}.json"

    @classmethod
    def get_s3_client(cls):
        return boto3.client("s3")


class TaskError(Exception):
    pass


def run_task():
    logger.info("running task")
    if random.randint(1, 100) <= 50:
        logger.info("❌ task failed")
        raise TaskError("random error")
    else:
        logger.info("✅ task succeeded")


tracker = MyTracker.new(id=1)
for _ in range(5):
    time.sleep(1)
    tracker = MyTracker.load(id=1)
    if tracker.status == StatusEnum.succeeded.value:
        break
    try:
        with tracker.start():
            run_task()
    except TaskError:
        pass
