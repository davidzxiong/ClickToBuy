# -*- coding: utf-8 -*-
# This is a controller class to control all the process

from PIL import Image
from worker import Worker
from utils import logger
#from flask.ext.sqlalchemy import SQLAlchemy

import ConfigParser
import error_def
import flask
import json
import numpy as np
import os
import sys
import uuid
import base64
import time

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
#db = SQLAlchemy(application)


@app.route("/")
def index():
    return flask.url_for('fetch_result', _method="GET")


@app.route("/error_code")
def error_code():
    return "Hello world"


@app.route("/query", methods=["POST"])
def fetch_result():
    results = dict()
    start_time = time.time()
    try:
        input_data = base64.decodestring(flask.request.form['data'])
        image_data = []
        width = 224
        height = 224
        for i in range(height):
            row = []
            for j in range(0, width * 4, 4):
                pixel = []
                for k in range(0, 3):
                    pixel.append(ord(input_data[i * width * 4 + j + k]))
                row.append(pixel)
            image_data.append(row)

    except Exception as e:
        results["error"] = "9998"
        logger.error("convert error")
        logger.error("%s" % e)
        return json.dumps(results)

    # image = Image.fromarray(np.array(image_data).astype('uint8'))
    # image.save("img.jpeg", "JPEG")
    decode_time = time.time()
    print("Decoding time is %.2f" % (decode_time - start_time))

    logger.error("%d" % len(image_data))
    logger.error("%d" % len(image_data[0]))
    logger.error("%d" % len(image_data[0][0]))

    try:
        product_url = worker.parse(np.array(image_data))
        results["url"] = str(product_url)
        logger.info("%s" % str(product_url))
    except Exception as e:
        results["error"] = "9999"
        logger.error("Parse error")
        logger.error("%s" % e)

    total_time = time.time()
    print("Image2Vector + GetURL time is %.2f" % (total_time - decode_time))
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
    #app.config['SQLALCHEMY_DATABASE_URI'] = config.get("db", "SQLALCHEMY_DATABASE_URI")
    app.run(
        host=host,
        port=port,
        use_reloader=True,
        processes=num_process)
