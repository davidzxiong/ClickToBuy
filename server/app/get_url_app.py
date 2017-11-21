# -*- coding: utf-8 -*-
# This is an app for find url in db.

from abstract_application import Application


class GetUrlApp(Application):
    def __init__(self, logger):
        super(GetUrlApp, self).__init__(logger)
        self._name = "GetUrl"

    def init(self, *args, **kwargs):
        return True

    def run(self, previous_result, *args, **kwargs):
        vector = previous_result
        if vector.shape[0] == 512:
            result = "https://amazon.com/id=1"
        return result, 0
