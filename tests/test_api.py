# -*- coding: utf-8 -*-

from abstract_tracker import api


def test():
    _ = api


if __name__ == "__main__":
    from abstract_tracker.tests import run_cov_test

    run_cov_test(__file__, "abstract_tracker.api", preview=False)
