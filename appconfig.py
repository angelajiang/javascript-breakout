class Config(object):
    DEBUG = False
    TESTING = False
    AVERAGESFILE = 'logs/average_hits'
    TABLEFILE = 'tables/current/large_table'
    TABLEDIR = 'tables/train'
    PERIOD = 1000000

class TestingConfig(Config):
    TESTING = True
    AVERAGESFILE = 'logs/average_hits_test'
    TABLEFILE = 'tables/current/large_table_test'
    TABLEDIR = 'tables/test'
    PERIOD = 100000

class DevConfig(Config):
    DEBUG = True
    AVERAGESFILE = 'logs/average_hits_dev'
    TABLEFILE = 'tables/current/large_table_debug'
    TABLEDIR = 'tables/debug'
