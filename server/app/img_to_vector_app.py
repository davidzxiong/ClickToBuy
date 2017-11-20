# -*- coding: utf-8 -*-
# Author: Jie Liu (liuj1229@gmail.com)
# This is an class for fetching pictures from specified hosts

from abstract_application import Application


class Image2VectorApp(Application):
    def __init__(self, logger):
        super(Image2VectorApp, self).__init__(logger)
        self._name = "Image2Vector"
        self._tmp_dir = None

    def init(self, *args, **kwargs):
        if len(args) > 0:
            self._tmp_dir = args[0]
        return True

    def run(self, previous_result, *args, **kwargs):
        image = args[0]
        result = [1]
        return result, 0
