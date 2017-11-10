# -*- coding: utf-8 -*-
# This is a test class to check the whole flow.

from abstract_application import Application


class TestApp(Application):
    def __init__(self, logger):
        super(TestApp, self).__init__(logger)
        self._name = "TestApp"

    def init(self, *args, **kwargs):
        return True

    def run(self, previous_result, *args, **kwargs):
        print "Hello world"
        if previous_result is None:
            print args
        result = dict()
        for arg in args:
            result[arg] = "good"
        return result
