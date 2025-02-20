# -*- coding: utf-8 -*-
class Config(object):
    DEBUG = False
    TESTING = False
    ARCHIVE_PATH = "/mnt"
    CAMERAS_CONFIG_FILE = "cameras.config"
    EXCEL_LIMIT_ROW = 1000
    EXCEL_TIME_LIVE = 600.0


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    ARCHIVE_PATH = "test"
    CAMERAS_CONFIG_FILE = "cameras-test.config"
