# -*- coding: utf-8 -*-
# This is a controller class to control all the process

from PIL import Image
from worker import Worker
from utils import logger

import ConfigParser
import error_def
import flask
import json
import numpy as np
import os
import sys
import uuid

config = ConfigParser.ConfigParser()


def _init_environment(config_file):
    if not os.path.isfile(config_file):
        print "Error: %s is not a regular file" % config_file
        sys.exit(1)
    config.read(config_file)

    if not os.path.exists("log"):
        os.mkdir("log")

    log_name = os.path.join(os.getcwd(), "log", config.get("log", "log_name"))
    # In debug mode, we want to keep the stream hanlder
    logger.set_file_handler(log_name,
                            config.getint("log", "max_size"),
                            config.getint("log", "backup_count"),
                            config.getboolean("server", "debug"))
    logger.set_level(config.get("log", "log_level"))
    
    sys.path.append("app/face_net/src")

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.url_for('fetch_result', _method="GET")


@app.route("/error_code")
def error_code():
    return "Hello world"


@app.route("/query", methods=["POST"])
def fetch_result():
    image = Image.open(flask.request.files['file'])
    image = image.resize((224, 224), Image.ANTIALIAS)
    #print "image is", type(image), image
    #image.show()
    image = np.array(image)
    #print image.shape
    results = dict()
    try:
        product_url = worker.parse(image)
        results["url"] = str(product_url)
        logger.info("%s" % str(product_url))
    except Exception as e:
        results["error"] = "9999"
        logger.error("Parse error")
        logger.error("%s" % e)
    # Convert results to json format
    return json.dumps(results)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Error, you need specify input file"
        sys.exit(1)

    _init_environment(sys.argv[1])
    worker = Worker(uuid.uuid1(), zip(*config.items("apps"))[1], logger)
    num_process = config.getint("server", "num_process")
    host = config.get("server", "listen_ip")
    port = config.getint("server", "port")
    logger.info("%d processes started on host %s" % (num_process, host))
    app.run(
        host=host,
        port=port,
        use_reloader=True,
        processes=num_process)
