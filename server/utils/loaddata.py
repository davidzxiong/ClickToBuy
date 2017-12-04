# -*- coding: utf-8 -*-
# The script load image embedding and url to json file.

import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torchvision
import json

from PIL import Image
from torch.autograd import Variable


cur_dir = os.path.dirname(__file__)
path = os.path.join(cur_dir, '..', 'images')
files = os.listdir(path)

id_url_table = pd.read_excel(os.path.join(path, 'id_url_table.xlsx'), dtype={'id':str, 'url':str})

model = torchvision.models.resnet101(pretrained=True)
model = nn.Sequential(*list(model.children())[:-1])


def img_to_vec(image):
    h, w, c = image.shape
    x = np.zeros([1, c, h, w])
    for i in xrange(c):
        x[0, i, :, :] = image[:, :, i]
    x = Variable(torch.from_numpy(x).float())
    result = model(x).data.numpy()[0, :, 0, 0]
    return result

data = dict()

for index, row in id_url_table.iterrows():
    filename = os.path.join(path, row['id'] + '.jpg')
    print filename
    img = Image.open(filename)
    img = img.resize((224, 224), Image.ANTIALIAS)
    img = np.array(img)
    vec = img_to_vec(img)
    key = ','.join(list(map(str, vec)))
    data[key] = row['id'][1] + row['url']
    print data[key]

with open(os.path.join(path, 'data.json'), 'w') as f:
    json.dump(data, f)





