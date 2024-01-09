About This Project
==============================================================================


Why this project
------------------------------------------------------------------------------
A task is an abstract concept in which an application is taking input data, processing the data, and generating some output.

When managing a large number of business-critical tasks, it’s crucial to monitor and identify which tasks have been successful, which have failed, and which are still in progress. If the business logic is a pipeline consisting of a sequence of tasks, it’s important to keep track of its current status and have the ability to recover from any failed task. We also have seen some advanced requirements from the community, such as the following:

- Each task should be consumed once and exactly once
- Each task should be handled by only one worker; you want a concurrency lock mechanism to avoid double consumption
- For succeeded tasks, you can store additional information such as the output, statistics, and metadata of the task, and log the success time
- For failed tasks, you can log the detailed error message for debugging
- You want to get all the failed tasks via one simple query and rerun with the updated business logic
- To avoid falling into an endless retry loop on tasks that are impossible to complete, you want to ignore the tasks if they fail too many times
- You want to run custom queries based on task status for analytics purpose

Typically, people use an RDBMS database to store task statuses. However, we have a way more options to choose from, depending on the specific use case. For instance, if a program is running locally, a simple JSON file can serve as a suitable backend. In cases where there aren't too many tasks but reliability is essential, AWS S3 can be employed as the backend storage solution. For scenarios involving a substantial volume of concurrent jobs, optimizing performance may require the use of a simple key-value store like AWS DynamoDB or Redis.

I am the author of the `pynamodb_mate <https://github.com/MacHu-GWU/pynamodb_mate-project/blob/master/examples/patterns/status-tracker.ipynb>`_ library, which is backed by DynamoDB. However, I want to extend this to support more backend. Instead, I have created this project to offer a common interface for various backend implementations, eliminating the need to reinvent the wheel for each one.


How to Use
------------------------------------------------------------------------------
:class:`~abstract_tracker.base.BaseTracker` serves as an abstract class and acts as the foundation for all tracker classes. It defines a common interface shared by all tracker classes, enabling you to create your own custom tracker class. Notably, the ``BaseTracker`` intentionally leaves the :meth:`~abstract_tracker.base.BaseTracker.load` and :meth:`~abstract_tracker.base.BaseTracker.dump` methods not implemented, allowing you to extend it and choose any backend for their implementation.

This library provides some concrete implementations of the tracker.

- :class:`~abstract_tracker.trackers.file_tracker.FileTracker` use a local file as the backend.
- :class:`~abstract_tracker.trackers.s3_tracker.S3Tracker` use AWS S3 as the backend


