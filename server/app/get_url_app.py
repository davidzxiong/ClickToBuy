# -*- coding: utf-8 -*-
# This is an app for find url in db.

from abstract_application import Application
import json
import os

import numpy as np
import time


class GetUrlApp(Application):
    def __init__(self, logger):
        super(GetUrlApp, self).__init__(logger)
        self._name = "GetUrl"
        cur_dir = os.path.dirname(__file__)
        path = os.path.join(cur_dir, '..', 'images')
        raw_data = json.load(open(os.path.join(path,'data.json'), 'r'))
        self.data = dict()
        for key, value in raw_data.items():
            key = tuple(map(float, key.split(',')))
            self.data[key] = value

    def init(self, *args, **kwargs):
        return True

    def run(self, previous_result, *args, **kwargs):
        start_time = time.time()
        vector = np.array(previous_result)
        min_dist = float('inf')
        result = None
        for key, value in self.data.items():
            if value[0] != '0': continue
            key = np.array(key)
            cur_dist = sum(np.power(key - vector, 2))
            if cur_dist < min_dist:
                min_dist = cur_dist
                result = value[1:]
        print "get url time is %.2f" % (time.time() - start_time)
        return result, 0
