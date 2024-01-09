# -*- coding: utf-8 -*-

import typing as T
import time
import shutil
import random
import dataclasses
from pathlib import Path

from abstract_tracker.logger import logger
from abstract_tracker.base import BaseStatusEnum
from abstract_tracker.trackers.file_tracker import T_ID, FileTracker

dir_data = Path(__file__).parent / "file_tracker"
shutil.rmtree(dir_data, ignore_errors=True)
dir_data.mkdir(parents=True, exist_ok=True)


class StatusEnum(BaseStatusEnum):
    pending = 0
    in_progress = 10
    failed = 20
    exhausted = 30
    succeeded = 40
    ignored = 50


@dataclasses.dataclass
class MyTracker(FileTracker):
    @classmethod
    def get_path(cls, id: T_ID) -> Path:
        return dir_data.joinpath(f"{id}.json")


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
