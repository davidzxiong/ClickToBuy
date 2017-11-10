# -*- coding: utf-8 -*-
# Author: Jie Liu (liuj1229@gmail.com)
# This is an class for fetching pictures from specified hosts

from abstract_application import Application

import urllib2


class Image2VectorApp(Application):
    def __init__(self, logger):
        super(Image2VectorApp, self).__init__(logger)
        self._name = "Image2Vector"

    def init(self, *args, **kwargs):
        if len(args) > 0:
            self._tmp_dir = args[0]
        return True

    def run(self, previous_result, *args, **kwargs):
        file_id = args[0]
        print("arg is what?", file_id)
        result = list()

        if file_id == u'1':
            print("file_id is 1")
            result = [1]
        elif file_id == u'2':
            result = [2]

        # save the pic temporally for debugging
        # try:
        #     fname = "%s/%s.jpg" % (self._tmp_dir, file_id)
        #     result.append(fname)
        #     with open(fname, "wb") as tmp_pic:
        #         tmp_pic.write(pic)
        # except Exception as e:
        #     return None, self._error_code + 2

        return result, 0
