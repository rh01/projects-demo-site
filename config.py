#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @license : Copyright(C), ReadAILib
# Created by ReadAILib.com on 2018/5/3

__author__ = 'shenhengheng'

import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "WTForm is What-The-F**k Form"


class DevelopmentConfig(Config):
    BOOTSTRAP_SERVE_LOCAL = True
    DEBUG = True


config = {
    "default": Config,
    "debug": DevelopmentConfig,
}

