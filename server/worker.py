# -*- coding: utf-8 -*-
# This is a controller class to control all the process

import importlib
import os
from utils import util


class Worker(object):
    def __init__(self, worker_id, apps, logger):
        self._swap_space = "/tmp/%s" % worker_id
        self._counter = 0
        self._clean_threshold = 1000
        self._logger = logger
        self._app_pipelines = list()
        self._app_index = dict()
        self._register_applications(apps)

    def _register_applications(self, apps):
        for app in apps:
            if isinstance(app, str):
                path = app.split(".")
                module_path = importlib.import_module(".".join(path[:-1]))
                method = getattr(module_path, path[-1])
                self._app_pipelines.append(method(self._logger))
            elif isinstance(app, type):
                self._app_pipelines.append(app())

        for index, app in enumerate(self._app_pipelines):
            self._app_index[app.name] = index
            app.set_id(index + 1)

        self._app_pipelines[self._app_index["Image2Vector"]].init(self._swap_space)

    def finalize(self, force_clean=False):
        # Delete all files when counter larger than threshold
        if force_clean or self._counter >= self._clean_threshold:
            util.clear_path(self._swap_space)

    def parse(self, *args, **kwargs):
        result = None
        self._counter += 1

        if not os.path.exists(self._swap_space):
            os.mkdir(self._swap_space)
        
        for app in self._app_pipelines:
            result, error_code = app.run(result, *args, **kwargs)
            if result is None or not result:
                self._logger.error("App:%s parse data error" % app.name)
                return error_code

        self.finalize()
        return result
