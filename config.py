class Config(object):
    DEBUG = False
    TESTING = False
    ARCHIVE_PATH = ""
    EXCEL_LIMIT_ROW = 1000

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True 
    ARCHIVE_PATH = "/test"
    