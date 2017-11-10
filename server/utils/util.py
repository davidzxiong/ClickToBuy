# -*- coding: utf-8 -*-

import os


def clear_path(path):
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
