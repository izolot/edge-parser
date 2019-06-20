class Config(object):
    DEBUG = False
    TESTING = False
    PARSE_PATH = "/home/ivan/Projects/larga/mnt"
    SERVER = ""
    PORT = ""


class DevelopmentConfig(Config):
    DEBUG = True
