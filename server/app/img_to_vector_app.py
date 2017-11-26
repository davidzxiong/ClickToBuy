# -*- coding: utf-8 -*-

from abstract_application import Application
from torch.autograd import Variable

import numpy as np
import torch
import torch.nn as nn
import torchvision

class Image2VectorApp(Application):
    def __init__(self, logger):
        super(Image2VectorApp, self).__init__(logger)
        self._name = "Image2Vector"
        self._tmp_dir = None
        self.model = torchvision.models.resnet101(pretrained=True)

    def init(self, *args, **kwargs):
        if len(args) > 0:
            self._tmp_dir = args[0]
        for param in self.model.parameters():
            param.requires_grad = False
        self.model = nn.Sequential(*list(self.model.children())[:-1])
        return True

    def run(self, previous_result, *args, **kwargs):
        image = args[0]
        h, w ,c = image.shape
        x = np.zeros([1,c,h,w])
        for i in xrange(c):
            x[0,i,:,:] = image[:,:,i]
        x = Variable(torch.from_numpy(x).float())
        result = self.model(x).data.numpy()[0,:,0,0]
        return result, 0
