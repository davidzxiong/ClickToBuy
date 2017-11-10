# -*- coding: utf-8 -*-
# Abstract class for all application
# All applications should derive from this class


class Application(object):
    def __init__(self, logger):
        self._name = "BaseApplication"
        self._logger = logger
        self._id = 0
        self._error_code = 0

    @property
    def name(self):
        return self._name

    def set_id(self, index):
        self._id = index
        self._error_code = index * 1000

    @property
    def id(self):
        return self._id

    def init(self, *args, **kwargs):
        raise NotImplementedError("You should call init function with derived class")

    def run(self, previous_result, *args, **kwargs):
        return previous_result
