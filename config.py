class Config(object):
    DEBUG = False
    TESTING = False
    PARSE_PATH = "/home/ivan/Projects/larga/mnt"
    SERVER = "127.0.0.1"
    PORT = "5000"


class DevelopmentConfig(Config):
    DEBUG = True








