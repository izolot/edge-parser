class Config(object):
    DEBUG = False
    TESTING = False
    ARCHIVE_PATH = ""

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True 