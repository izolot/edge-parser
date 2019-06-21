class Config(object):
    DEBUG = False
    TESTING = False
    ARCHIVE_PATH = "/Users/ivangrimm/Documents/mnt"
    HOST = "127.0.0.1"
    PORT = "5551"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True 